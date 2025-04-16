from dataclasses import dataclass
from datetime import datetime

@dataclass
class DirectoryChangeEvent:
    """
    Represents a file system change event.

    :param action: Type of action ('created', 'deleted', etc.).
    :param full_path: Full path to the changed file.
    :param base_path: Watched directory base path.
    :param file_name: Name of the file that changed.
    :param timestamp: Time when the event occurred.
    """
    action: str
    full_path: str
    base_path: str
    file_name: str
    timestamp: datetime