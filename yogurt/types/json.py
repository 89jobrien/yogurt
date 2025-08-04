from typing import Any, Dict, List, Union

# Basic recursive JSON type
JSONPrimitive = Union[str, int, float, bool, None]
JSONType = Union[JSONPrimitive, Dict[str, Any], List[Any]]
# For stricter, recursive types:
JSON = Union[
    JSONPrimitive,
    List["JSON"],     # type: ignore  # recursive definition for Mypy
    Dict[str, "JSON"] # type: ignore
]