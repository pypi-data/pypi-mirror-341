from .config_parser import Config
from .config_writer import write_config
from types import SimpleNamespace

__all__ = ["parse_config", "write_config"]

def parse_config() -> SimpleNamespace:
    """
    Retrieves the application configuration, including both YAML, JSON, TOM and .env content.

    :return: A namespace object with config and env values accessible via dot notation.
    """
    return Config().get()