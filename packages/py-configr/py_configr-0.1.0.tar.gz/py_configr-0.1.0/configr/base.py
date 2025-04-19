"""
Configuration management base module.

This module provides a generic framework for loading, parsing, and validating
configuration files of different formats (JSON, YAML). It handles the conversion
of configuration data to strongly typed dataclass instances, with support for
nested dataclasses and complex type validation.

The module includes:
- ConfigBase class: The main class for loading and validating configuration
- Type validation utilities
- Support for different configuration file formats

Typical usage:
    @config_class(file_name="database")
    class DatabaseConfig:
        host: str
        port: int = 5432

    config = ConfigBase.load(DatabaseConfig)
"""
import dataclasses
import os
from collections.abc import Iterable
from pathlib import Path
from typing import ClassVar, Generic, TypeVar, get_args

from .exceptions import ConfigFileNotFoundError, ConfigValidationError
from .field_type_checker import FieldTypeChecker
from .loaders import ConfigLoader, JSONConfigLoader, YAMLConfigLoader

T = TypeVar('T')


class ConfigBase(Generic[T]):
    """
    Base class for configuration management.

    Handles loading configuration from files and conversion to dataclasses.
    """

    _config_dir: ClassVar[str] = os.environ.get('CONFIG_DIR', '_config')
    _loaders: ClassVar[dict[str, type[ConfigLoader]]] = {
        '.json': JSONConfigLoader,
        '.yaml': YAMLConfigLoader,
        '.yml': YAMLConfigLoader
    }

    @classmethod
    def set_config_dir(cls, config_dir: str | Path) -> None:
        """Set the base config directory path if default should not be used."""
        if isinstance(config_dir, Path):
            cls._config_dir = str(config_dir)
        else:
            cls._config_dir = config_dir

    @classmethod
    def get_available_loaders(cls) -> dict[str, type[ConfigLoader]]:
        """Get available loaders for different file extensions."""
        return cls._loaders

    @classmethod
    def add_loader(cls, ext: str, loader: type[ConfigLoader]) -> None:
        """Add a loader for a specific file extension."""
        if ext not in cls._loaders:
            cls._loaders[ext] = loader

    @classmethod
    def remove_loader(cls, ext: str) -> None:
        """Remove a loader for a specific file extension."""
        if ext in cls._loaders:
            del cls._loaders[ext]

    @classmethod
    def get_config_path(cls) -> Path:
        """Get the base configuration directory path."""
        return Path(cls._config_dir)

    @classmethod
    def load(cls, config_class: type[T], config_data: dict | None = None) -> T:
        """
        Load configuration from file and convert to the specified dataclass.

        Args:
            config_class: The dataclass to convert configuration to
            config_data: Optional dictionary with configuration data, if it
                         is not provided, the configuration will be loaded
                         from file. This is mostly needed for recursive
                         loading of nested dataclasses.

        Returns:
            An instance of the specified dataclass with loaded configuration
        """
        # Ensure config_class is a dataclass
        if not dataclasses.is_dataclass(config_class):
            raise TypeError(f"{config_class.__name__} must be a dataclass")

        if config_data is None:
            config_data = cls.__read_config_data_from_file(config_class)

        # Convert to dataclass
        # Filter config_data to only include fields defined in the dataclass
        fields = {f.name: f.type for f in dataclasses.fields(config_class)}
        field_names = fields.keys()
        filtered_data = {k: v for k, v in config_data.items()
                         if k in field_names}

        data = cls.__load_nested_dataclasses(fields, filtered_data)
        try:
            FieldTypeChecker.check_types(fields, filtered_data)
        except TypeError as exc:
            raise ConfigValidationError(f"Configuration validation failed: "
                                        f"{exc}") from exc

        # Create an instance of the dataclass
        return config_class(**data)

    @classmethod
    def __read_config_data_from_file(cls, config_class):
        """Read configuration data from file and return as a dictionary."""
        file_name = cls._get_config_file_name(config_class)
        config_file_path = cls._get_config_file_path(file_name)
        loader = cls._get_loader(config_file_path)

        config_data = loader.load(config_file_path)

        return config_data

    @classmethod
    def __load_nested_dataclasses(cls, fields: dict[str, type], data: dict) -> dict:
        """Recursively load nested dataclasses."""
        for key, value in data.items():
            field_type = fields[key]
            if dataclasses.is_dataclass(field_type):
                if isinstance(value, dict):
                    data[key] = cls.load(field_type, value)
                elif value is None:
                    # Try to create a new (empty) instance of nested dataclass
                    # if value is None.
                    # This only works if the nested dataclass has no required arguments,
                    # otherwise the value will remain None
                    try:
                        data[key] = field_type()
                    except TypeError:
                        pass
            elif isinstance(value, Iterable):
                origin_types = get_args(field_type)
                if origin_types and dataclasses.is_dataclass(origin_types[0]):
                    for i, value_elem in enumerate(value):
                        if isinstance(value_elem, dict):
                            value[i] = cls.load(origin_types[0], value_elem)
                    data[key] = value

        return data

    @classmethod
    def _get_loader(cls, file_name):
        """Determine loader from file extension."""
        ext = Path(file_name).suffix

        if ext not in cls._loaders:
            raise ValueError(f"Unsupported file extension: {ext}. Supported: "
                             f"{list(cls._loaders.keys())}")

        return cls._loaders[ext]()

    @classmethod
    def _get_config_file_path(cls, file_name: str) -> Path:
        """Get full path to config file."""
        config_file_path = cls.get_config_path() / file_name

        # If file_name does not have a suffix, iterate over all
        # available extensions and find the first one that exists
        if Path(file_name).suffix == '':
            for ext in cls._loaders:
                config_file_path = cls.get_config_path() / (file_name + ext)
                if config_file_path.exists():
                    return config_file_path

        if not config_file_path.exists():
            raise ConfigFileNotFoundError(f"Configuration file not found: "
                                          f"{config_file_path}")

        return config_file_path

    @classmethod
    def _get_config_file_name(cls, config_class: type) -> str:
        """Get file name from config class."""
        if hasattr(config_class, '_config_file_name'):
            file_name = config_class._config_file_name
        else:
            raise ValueError(f"{config_class.__name__} must have a "
                             f"_config_file_name attribute")
        return file_name
