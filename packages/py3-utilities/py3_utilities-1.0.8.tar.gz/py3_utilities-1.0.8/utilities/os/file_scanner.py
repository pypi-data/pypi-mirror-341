import asyncio
import os
import re
import logging

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncGenerator, Callable, List, Optional, Tuple, Union
from enum import Enum, unique
from datetime import datetime
from collections import deque

from ..utility_base import UtilityBase
from ..logger import Logger, LogWrapper


@unique
class TraversalMethod(Enum):
    """
    Enum to define traversal methods.
    """
    BFS = "BFS"
    DFS = "DFS"


class FileScanner(UtilityBase):
    """
    Asynchronously scans files in a directory structure based on given criteria.
    """

    def __init__(
        self,
        root_dir: Union[str, Path],
        max_workers: int = 16,
        method: TraversalMethod = TraversalMethod.BFS,
        file_patterns: Optional[List[str]] = None,
        folder_patterns: Optional[List[str]] = None,
        first_folder_patterns: Optional[List[str]] = None,
        max_depth: Optional[int] = None,
        min_file_size: Optional[int] = None,
        modified_after: Optional[datetime] = None,
        match_callback: Optional[Callable[[str], None]] = None,
        skip_hidden: bool = True,
        follow_symlinks: bool = False,
        verbose: bool = False,
        logger: Optional[Union[logging.Logger, Logger, LogWrapper]] = None,
        log_level: Optional[int] = None
    ):
        """
        Initializes the file scanner.

        :param root_dir: Root directory to start scanning.
        :param max_workers: Maximum number of concurrent workers.
        :param method: Traversal method (BFS or DFS).
        :param file_patterns: List of regex patterns to match file names.
        :param folder_patterns: List of regex patterns to match folder names.
        :param first_folder_patterns: List of regex patterns to match folder names directly under root (depth = 1 folders).
        :param max_depth: Maximum depth to traverse.
        :param min_file_size: Minimum file size in bytes to include.
        :param modified_after: Include files modified after this datetime.
        :param match_callback: A function to be called when a file is found.
        :param skip_hidden: Skip hidden files and folders if True.
        :param follow_symlinks: Follow symbolic links if True.
        :param verbose: If True, logs the files during the search.
        :param logger: Optional logger instance. If not provided, a default logger is used.
        :param log_level: Optional log level. If not provided INFO level will be used for logging
        """
        # Init base class
        super().__init__(verbose, logger, log_level)

        self.root_dir = Path(root_dir)
        self.max_workers = max_workers
        self.method = method
        self.file_patterns = [re.compile(p, re.IGNORECASE) for p in file_patterns] if file_patterns else []
        self.folder_patterns = [re.compile(p, re.IGNORECASE) for p in folder_patterns] if folder_patterns else []
        self.first_folder_patterns =  [re.compile(p, re.IGNORECASE) for p in first_folder_patterns] if first_folder_patterns else []
        self.max_depth = max_depth
        self.match_callback = match_callback
        self.min_file_size = min_file_size
        self.modified_after = modified_after
        self.skip_hidden = skip_hidden
        self.follow_symlinks = follow_symlinks

    async def scan_files(self) -> AsyncGenerator[Path, None]:
        """
        Starts asynchronous scanning of files.

        :yield: Path objects of files that match the criteria.
        """
        loop = asyncio.get_running_loop()

        self._log(f"Scanning `{self.root_dir}`, with {self.method} method.")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if self.method == TraversalMethod.BFS:
                async for path in self._scan_bfs(loop, executor):
                    yield path
            elif self.method == TraversalMethod.DFS:
                async for path in self._scan_dfs(loop, executor):
                    yield path

    async def _scan_bfs(self, loop, executor) -> AsyncGenerator[Path, None]:
        """
        Performs asynchronous breadth-first scanning.

        :param loop: Event loop.
        :param executor: Thread pool executor.
        :yield: Path objects for files found.
        """
        queue = deque([(self.root_dir, 0)])

        while queue:
            tasks = []
            while queue and len(tasks) < self.max_workers:
                tasks.append(queue.popleft())

            futures = [loop.run_in_executor(executor, self._walk_fast, path, depth) for path, depth in tasks]

            for future in asyncio.as_completed(futures):
                subdirs, files, depth = await future
                if self.max_depth is None or depth < self.max_depth:
                    queue.extend([(subdir, depth + 1) for subdir in subdirs])

                for file in files:
                    yield Path(file)

    async def _scan_dfs(self, loop, executor) -> AsyncGenerator[Path, None]:
        """
        Performs asynchronous depth-first scanning.

        :param loop: Event loop.
        :param executor: Thread pool executor.
        :yield: Path objects for files found.
        """
        stack = [(self.root_dir, 0)]

        while stack:
            current_dir, current_depth = stack.pop()

            if self.max_depth is not None and current_depth > self.max_depth:
                continue

            subdirs, files, _ = await loop.run_in_executor(executor, self._walk_fast, current_dir, current_depth)

            for file in files:
                yield Path(file)

            stack.extend([(Path(sd), current_depth + 1) for sd in reversed(subdirs)])

    def _walk_fast(self, directory: Path, depth: int) -> Tuple[List[Path], List[Path], int]:
        """
        Quickly scans a directory, returning subdirectories and matching files.

        :param directory: Directory to scan.
        :param depth: Current depth.
        :return: Tuple of subdirectories, matching files, and current depth.
        """
        subdirs, files = [], []
        try:
            with os.scandir(directory) as it:
                for entry in it:
                    if self.skip_hidden and entry.name.startswith('.'):
                        continue
                    if entry.is_symlink() and not self.follow_symlinks:
                        continue

                    entry_path = Path(entry.path)

                    if entry.is_dir(follow_symlinks=self.follow_symlinks):
                        if depth == 0:
                            if not self.first_folder_patterns or self._matches_patterns(entry.name, self.first_folder_patterns):
                                subdirs.append(entry_path)
                        else:
                            if not self.folder_patterns or self._matches_patterns(entry.name, self.folder_patterns):
                                subdirs.append(entry_path)
                    elif entry.is_file(follow_symlinks=self.follow_symlinks):
                        if not self.file_patterns or self._matches_patterns(entry.name, self.file_patterns):
                            stat = entry.stat(follow_symlinks=self.follow_symlinks)

                            if self._passes_stat_filters(stat):
                                self._log(f"File found: `{entry_path}`")
                                if self.match_callback:
                                    self.match_callback(entry_path) 

                                files.append(entry_path)

        except OSError as e:
            self.logger.warning(f"Can't scan directory: {directory}: {e}")

        return subdirs, files, depth

    def _matches_patterns(self, name: str, patterns: List[re.Pattern]) -> bool:
        """
        Checks if the given name matches any of the provided regex patterns.

        :param name: Name to check.
        :param patterns: List of compiled regex patterns.
        :return: True if a match is found.
        """
        return any(p.search(name) for p in patterns)

    def _passes_stat_filters(self, stat) -> bool:
        """
        Checks if a file's statistics pass the filtering criteria.

        :param stat: File statistics object.
        :return: True if file meets criteria.
        """
        if self.min_file_size and stat.st_size < self.min_file_size:
            return False
        
        if self.modified_after and datetime.fromtimestamp(stat.st_mtime) < self.modified_after:
            return False
        
        return True
