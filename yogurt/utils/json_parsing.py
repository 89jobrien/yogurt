import json
import re
from typing import Any, Callable


def _replace_newline(match: re.Match[str]) -> str:
    """Replaces unescaped newlines, tabs, and quotes in a string."""
    value = match.group(2)
    value = re.sub(r"\n", r"\\n", value)
    value = re.sub(r"\r", r"\\r", value)
    value = re.sub(r"\t", r"\\t", value)
    value = re.sub(r'(?<!\\)"', r'\\"', value)
    return match.group(1) + value + match.group(3)


def _custom_parser(multiline_string: str) -> str:
    """
    Applies the custom newline and quote replacement to the action_input
    field within a JSON string.
    """
    if isinstance(multiline_string, (bytes, bytearray)):
        multiline_string = multiline_string.decode()

    return re.sub(
        r'("action_input"\:\s*")(.*?)(")',
        _replace_newline,
        multiline_string,
        flags=re.DOTALL,
    )


def parse_partial_json(s: str, *, strict: bool = False) -> Any:
    """
    Parses a JSON string that may be missing closing braces by attempting
    to fix it.
    """
    try:
        return json.loads(s, strict=strict)
    except json.JSONDecodeError:
        pass

    new_chars = []
    stack = []
    is_inside_string = False
    escaped = False

    for char in s:
        new_char = char
        if is_inside_string:
            if char == '"' and not escaped:
                is_inside_string = False
            elif char == "\\n" and not escaped:
                new_char = "\\\\n"
            elif char == "\\":
                escaped = not escaped
            else:
                escaped = False
        elif char == '"':
            is_inside_string = True
            escaped = False
        elif char == "{":
            stack.append("}")
        elif char == "[":
            stack.append("]")
        elif char in {"}", "]"}:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                return None
        new_chars.append(new_char)

    if is_inside_string:
        if escaped:
            new_chars.pop()
        new_chars.append('"')

    stack.reverse()
    # Attempt to parse by progressively removing characters from the end
    while new_chars:
        try:
            return json.loads("".join(new_chars + stack), strict=strict)
        except json.JSONDecodeError:
            new_chars.pop()

    return None  # Return None if parsing fails completely


def parse_json_markdown(
    json_string: str, *, parser: Callable[[str], Any] = parse_partial_json
) -> dict:
    """
    Parses a JSON string from a Markdown string, cleaning it up and
    handling partial JSON.
    """
    # Find JSON string within triple backticks
    match = re.search(r"```(json)?\s*\n(.*?)\n```", json_string, re.DOTALL)
    if match:
        json_str = match.group(2)
    else:
        json_str = json_string

    # Strip whitespace, newlines, and backticks
    json_str = json_str.strip(" \n\r\t`")

    # Handle special characters inside the value
    json_str = _custom_parser(json_str)

    # Parse the cleaned string
    return parser(json_str)
