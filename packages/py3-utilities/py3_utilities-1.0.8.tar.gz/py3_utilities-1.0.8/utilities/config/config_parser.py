import os
import yaml
import tomllib
import json
import configparser
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Union, Dict


class Config:
    """
    A singleton class that loads and provides access to application configuration.

    It loads environment variables from a `.env` file and merges configuration from
    all `*.yaml`, `*.yml`, `*.toml`, `*.xml` or `*.json` files, in the current directory.
    """
    _instance = None
    _config: SimpleNamespace

    def __new__(cls) -> "Config":
        """
        Creates a singleton instance of the Config class.

        :return: A singleton Config instance.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self) -> None:
        """
        Loads environment variables from `.env` and configuration from all matching config files.

        Merges configuration from all YAML, TOML, and JSON files that contain 'config' in their filename.
        """
        # Load .env
        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

        # Map environment variables
        env_vars = {
            key: value for key, value in os.environ.items()
            if key.isidentifier()
        }
        self._env = self._dict_to_namespace(env_vars)

        # Collect and merge all configs
        config_files = (
            sorted(Path(".").glob("*.toml")) +
            sorted(Path(".").glob("*.yaml")) +
            sorted(Path(".").glob("*.yml"))  +
            sorted(Path(".").glob("*.json")) +
            sorted(Path(".").glob("*.ini"))  +
            sorted(Path(".").glob("*.xml"))
        )

        merged_config: Dict[str, Any] = {}

        for file_path in config_files:
            if file_path.suffix == ".ini":
                parser = configparser.ConfigParser()
                parser.read(file_path)
                data = {section: dict(parser[section]) for section in parser.sections()}
            else:
                with open(file_path, "rb") as f:
                    if file_path.suffix in [".yaml", ".yml"]:
                        data = yaml.safe_load(f)
                    elif file_path.suffix == ".toml":
                        data = tomllib.load(f)
                    elif file_path.suffix == ".json":
                        data = json.load(f)
                    elif file_path.suffix == ".xml":
                        tree = ET.parse(f)
                        root = tree.getroot()
                        data = self._xml_to_dict(root)
                    else:
                        continue

            if data:
                merged_config = self._deep_merge_dicts(merged_config, data)

        self._config = self._dict_to_namespace(merged_config)

    def _xml_to_dict(self, elem: ET.Element) -> Dict[str, Any]:
        """
        Recursively converts an XML element and its children into a dictionary,
        merging attributes as regular keys.

        :param elem: The XML element to convert.
        :return: A dictionary representation of the XML tree.
        """
        d = {}

        # Process children
        children = list(elem)
        if children:
            child_dict = {}
            for child in children:
                child_data = self._xml_to_dict(child)
                for k, v in child_data.items():
                    if k in child_dict:
                        if not isinstance(child_dict[k], list):
                            child_dict[k] = [child_dict[k]]
                        child_dict[k].append(v)
                    else:
                        child_dict[k] = v
            d.update(child_dict)

        # Add attributes directly
        if elem.attrib:
            d.update({k.lower(): v for k, v in elem.attrib.items()})

        # Add text content if no children
        text = elem.text.strip() if elem.text else ""
        if text and not children:
            d["value"] = text

        return {elem.tag.lower(): d or text}

    def _deep_merge_dicts(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merges two dictionaries.

        :param base: The base dictionary to merge into.
        :param override: The dictionary with override values.
        :return: A merged dictionary with nested updates.
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge_dicts(result[key], value)
            else:
                result[key] = value
        return result

    def _dict_to_namespace(self, d: Any) -> Union[SimpleNamespace, list, Any]:
        """
        Recursively converts a dictionary to a nested SimpleNamespace.

        :param d: The dictionary or list to convert.
        :return: A nested structure with SimpleNamespaces for dicts.
        """
        if isinstance(d, dict):
            return SimpleNamespace(**{str(k).lower(): self._dict_to_namespace(v) for k, v in d.items()})
        elif isinstance(d, list):
            return [self._dict_to_namespace(i) for i in d]
        else:
            return d

    def get(self) -> SimpleNamespace:
        """
        Retrieves the loaded configuration with an additional 'env' namespace.

        :return: A namespace with config plus an `env` namespace inside.
        """
        cfg = self._config
        setattr(cfg, "os", SimpleNamespace())
        setattr(cfg.os, "env", self._env)
        return cfg

    def reload(self) -> None:
        """
        Reloads the configuration from the `.env` and matching YAML/TOML/JSON files.

        This is useful if the configuration files are updated while the application is running.
        """
        self._load()
