import asyncio
import threading
import win32file
import win32con
import os
import logging
import fnmatch

from typing import Callable, Optional, AsyncGenerator, Tuple, List, Union, Dict
from datetime import datetime
from pathlib import Path

from ..utility_base import UtilityBase
from ..logger import Logger, LogWrapper
from .directory_event import DirectoryChangeEvent


class DirectoryWatcherWindows(UtilityBase):
    """
    Watches a directory for file system changes on Windows using the Win32 API.
    """

    ACTIONS = {
        1: "created",
        2: "deleted",
        3: "modified",
        4: "renamed_from",
        5: "renamed_to"
    }

    def __init__(
        self,
        path: Union[str, Path],
        recursive: bool = True,
        notify_filter: Optional[int] = None,
        buffer_size: int = 1024,
        poll_interval: float = 1.0,
        debounce_interval: float = 1.0,
        file_patterns: Optional[List[str]] = None,
        event_callback: Callable[[DirectoryChangeEvent], None] = None,
        verbose: bool = False,
        logger: Optional[Union[logging.Logger, Logger, LogWrapper]] = None,
        log_level: Optional[int] = None,
        max_retries: int = 3
    ) -> None:
        """
        Initializes the DirectoryWatcher.

        :param path: Directory path to monitor.
        :param recursive: Whether to watch subdirectories.
        :param notify_filter: Bitmask specifying change notifications.
        :param buffer_size: Buffer size for change events.
        :param poll_interval: Polling interval in seconds.
        :param debounce_interval: Interval to suppress duplicate events.
        :param file_patterns: Glob patterns to match file names.
        :param event_callback: Function to call on directory events.
        :param verbose: Enable verbose logging.
        :param logger: Optional logger instance.
        :param log_level: Logging level.
        :param max_retries: Maximum handle recovery attempts.
        """
        super().__init__(verbose, logger, log_level)

        self.path = str(path)
        self.recursive = recursive
        self.buffer_size = buffer_size
        self.poll_interval = poll_interval
        self.debounce_interval = debounce_interval
        self.file_patterns = file_patterns or ["*"]
        self.notify_filter = notify_filter or (
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
        )

        self._stop_event = threading.Event()
        self._handle: Optional[int] = None
        self._event_cache: Dict[str, datetime] = {}
        self.max_retries = max_retries
        self.callback = event_callback

        self._open_handle()

    def _open_handle(self) -> None:
        """
        Opens a file handle for the directory using the Win32 API.
        """
        try:
            self._handle = win32file.CreateFile(
                self.path,
                win32con.GENERIC_READ,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None
            )
        except Exception as e:
            self._handle = None
            self.logger.error(f"Failed to open handle for '{self.path}': {e}", exc_info=True)

    async def watch(self) -> AsyncGenerator[DirectoryChangeEvent, None]:
        """
        Asynchronously watches the directory and yields change events.

        :yield: DirectoryChangeEvent for each detected change.
        """
        self._stop_event.clear()

        while not self._stop_event.is_set():
            if not self._handle:
                await asyncio.sleep(self.poll_interval)
                continue

            try:
                results = await asyncio.get_running_loop().run_in_executor(None, self._read_changes)
                now = datetime.now()

                for action, file_name in results:
                    full_path = os.path.join(self.path, file_name)
                    
                    if not any(fnmatch.fnmatch(file_name, pat) for pat in self.file_patterns):
                        continue  # Skip non-matching files

                    last_event = self._event_cache.get(full_path)
                    if last_event and (now - last_event).total_seconds() < self.debounce_interval:
                        continue  # Skip duplicate events

                    self._event_cache[full_path] = now
                    action_str = self.ACTIONS.get(action, "unknown")
                    self._log(f"{action_str} -> {file_name}")

                    event = DirectoryChangeEvent(
                        action=action_str,
                        full_path=full_path,
                        base_path=self.path,
                        file_name=file_name,
                        timestamp=now
                    )

                    if self.callback:
                        self.callback(event)

                    yield event

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.critical(f"Unexpected error in watch loop: {e}", exc_info=True)
                self._stop_event.set()

    def _read_changes(self) -> List[Tuple[int, str]]:
        """
        Reads directory changes using the Win32 API.

        :return: List of (action, file_name) tuples.
        """
        try:
            results = win32file.ReadDirectoryChangesW(
                self._handle,
                self.buffer_size,
                self.recursive,
                self.notify_filter,
                None,
                None
            )
            return results
        except Exception as e:
            self.logger.critical(f"ReadDirectoryChangesW failed for '{self.path}': {e}", exc_info=True)
            self._recover_handle()
            return []

    def _recover_handle(self) -> None:
        """
        Attempts to recover the file handle if it becomes invalid.
        """
        self.logger.warning(f"Attempting to recover handle for '{self.path}'...")
        retries = 0

        while retries < self.max_retries:
            try:
                self._open_handle()
                if self._handle:
                    self.logger.warning(f"Recovered handle for '{self.path}'")
                    return
            except Exception as e:
                self.logger.warning(f"Retry {retries + 1} failed for '{self.path}': {e}")
            retries += 1

        self.logger.critical(f"Failed to recover handle for '{self.path}' after {self.max_retries} retries")
        self._handle = None

    def close(self) -> None:
        """
        Stops watching and closes the directory handle.
        """
        self._stop_event.set()
        try:
            if self._handle:
                win32file.CloseHandle(self._handle)
                self._log(f"Closed handle for '{self.path}'")
        except Exception as e:
            self.logger.critical(f"Failed to close handle for '{self.path}': {e}", exc_info=True)
        self._handle = None

    def __enter__(self) -> "DirectoryWatcherWindows":
        """
        Enters a context manager block.

        :return: Self instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits a context manager block and cleans up resources.

        :param exc_type: Exception type.
        :param exc_value: Exception value.
        :param traceback: Exception traceback.
        """
        self.close()
