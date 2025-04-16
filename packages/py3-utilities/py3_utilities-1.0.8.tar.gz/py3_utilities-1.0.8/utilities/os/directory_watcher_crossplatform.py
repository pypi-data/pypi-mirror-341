import asyncio
import fnmatch
import logging
import os
from datetime import datetime
from pathlib import Path
from threading import Thread, Event
from typing import Callable, Optional, AsyncGenerator, List, Union, Dict

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileSystemMovedEvent

from ..utility_base import UtilityBase
from ..logger import Logger, LogWrapper
from .directory_event import DirectoryChangeEvent


class DirectoryWatcherCrossplatform(UtilityBase):
    """
    Cross-platform directory watcher using the watchdog library.
    """

    def __init__(
        self,
        path: Union[str, Path],
        recursive: bool = True,
        debounce_interval: float = 1.0,
        file_patterns: Optional[List[str]] = None,
        event_callback: Callable[[DirectoryChangeEvent], None] = None,
        verbose: bool = False,
        logger: Optional[Union[logging.Logger, Logger, LogWrapper]] = None,
        log_level: Optional[int] = None,
    ) -> None:
        """
        Initializes the DirectoryWatcherCrossplatform.

        :param path: Directory path to monitor.
        :param recursive: Whether to watch subdirectories.
        :param debounce_interval: Interval to suppress duplicate events.
        :param file_patterns: Glob patterns to match file names.
        :param event_callback: Function to call on directory events.
        :param verbose: Enable verbose logging.
        :param logger: Optional logger instance.
        :param log_level: Logging level.
        """
        super().__init__(verbose, logger, log_level)

        self.path = str(path)
        self.recursive = recursive
        self.debounce_interval = debounce_interval
        self.file_patterns = file_patterns or ["*"]
        self.callback = event_callback

        self._event_cache: Dict[str, datetime] = {}
        self._stop_event = Event()
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._observer = Observer()
        self._handler = self._create_handler()

        self._observer.schedule(self._handler, self.path, recursive=self.recursive)
        self._thread = Thread(target=self._observer.run, daemon=True)
        self._thread.start()

    def _create_handler(self) -> FileSystemEventHandler:
        watcher = self

        class Handler(FileSystemEventHandler):
            def dispatch(self, event: FileSystemEvent) -> None:
                try:
                    if event.is_directory:
                        return

                    file_name = os.path.basename(event.src_path)
                    if not any(fnmatch.fnmatch(file_name, pat) for pat in watcher.file_patterns):
                        return

                    full_path = event.src_path
                    now = datetime.now()
                    last_event = watcher._event_cache.get(full_path)

                    if last_event and (now - last_event).total_seconds() < watcher.debounce_interval:
                        return  # Debounce

                    watcher._event_cache[full_path] = now

                    if isinstance(event, FileSystemMovedEvent):
                        action = "renamed_to"
                        file_name = os.path.basename(event.dest_path)
                        full_path = event.dest_path
                    elif event.event_type == "created":
                        action = "created"
                    elif event.event_type == "deleted":
                        action = "deleted"
                    elif event.event_type == "modified":
                        action = "modified"
                    else:
                        action = "unknown"

                    watcher._log(f"{action} -> {file_name}")

                    change_event = DirectoryChangeEvent(
                        action=action,
                        full_path=full_path,
                        base_path=watcher.path,
                        file_name=file_name,
                        timestamp=now
                    )

                    if watcher.callback:
                        watcher.callback(change_event)

                    asyncio.run_coroutine_threadsafe(
                        watcher._event_queue.put(change_event), asyncio.get_event_loop()
                    )

                except Exception as e:
                    watcher.logger.error(f"Failed to process event: {e}", exc_info=True)

        return Handler()

    async def watch(self) -> AsyncGenerator[DirectoryChangeEvent, None]:
        """
        Asynchronously yields file system events.

        :yield: DirectoryChangeEvent for each detected change.
        """
        while not self._stop_event.is_set():
            try:
                event = await self._event_queue.get()
                yield event
            except Exception as e:
                self.logger.error(f"Error yielding directory event: {e}", exc_info=True)
                break

    def close(self) -> None:
        """
        Stops watching and cleans up resources.
        """
        self._stop_event.set()
        try:
            self._observer.stop()
            self._observer.join()
            self._log(f"Stopped observer for '{self.path}'")
        except Exception as e:
            self.logger.critical(f"Failed to stop observer for '{self.path}': {e}", exc_info=True)

    def __enter__(self) -> "DirectoryWatcherCrossplatform":
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
