import json
from pathlib import Path
from typing import Type, Union, Dict, Any
from pydantic import BaseModel, ValidationError

try:
    import tomli
except ImportError:
    tomli = None

try:
    import yaml
except ImportError:
    yaml = None


def load_config_file(path: Union[str, Path]) -> Dict[str, Any]:
    path = Path(path)
    ext = path.suffix.lower()

    if ext == ".json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    elif ext in {".yaml", ".yml"}:
        if yaml is None:
            raise ImportError(
                "PyYAML is required to load YAML files. Install with `pip install pyyaml`."
            )
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    elif ext == ".toml":
        if tomli is None:
            raise ImportError(
                "tomli is required to load TOML files. Install with `pip install tomli`."
            )
        with path.open("rb") as f:
            return tomli.load(f)

    else:
        raise ValueError(f"Unsupported configuration file extension: '{ext}'")


def load_settings(
    settings_model: Type[BaseModel], config_path: Union[str, Path]
) -> BaseModel:
    data = load_config_file(config_path)
    try:
        return settings_model(**data)
    except ValidationError as e:
        print(f"Error parsing config file {config_path}:\n{e}")
        raise
