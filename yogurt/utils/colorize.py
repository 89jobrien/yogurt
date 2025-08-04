from typing import Optional, TextIO

_TEXT_COLOR_MAPPING = {
    "black": "30;1",
    "red": "31;1",
    "green": "32;1",
    "yellow": "33;1",
    "blue": "34;1",
    "magenta": "35;1",
    "cyan": "36;1",
    "white": "37;1",
    "bright_black": "90;1",
    "bright_red": "91;1",
    "bright_green": "92;1",
    "bright_yellow": "93;1",
    "bright_blue": "94;1",
    "bright_magenta": "95;1",
    "bright_cyan": "96;1",
    "bright_white": "97;1",
    # 256-color
    "pink": "38;5;200",
    "orange": "38;5;208",
    "turquoise": "38;5;80",
    "lime": "38;5;154",
    "violet": "38;5;141",
    "gold": "38;5;220",
    "salmon": "38;5;209",
    "peach": "38;5;214",
    "teal": "38;5;30",
    "lavender": "38;5;147",
}



def get_color_mapping(
    items: list[str], excluded_colors: Optional[list] = None
) -> dict[str, str]:
    colors = list(_TEXT_COLOR_MAPPING.keys())
    if excluded_colors is not None:
        colors = [c for c in colors if c not in excluded_colors]
    return {item: colors[i % len(colors)] for i, item in enumerate(items)}


def get_colored_text(text: str, color: str) -> str:
    color_str = _TEXT_COLOR_MAPPING[color]
    if not color_str:
        raise ValueError(f"Unknown color '{color}'")
    return f"\u001b[{color_str}m\033[1;3m{text}\u001b[0m"


def get_bolded_text(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def print_text(
    text: str,
    color: Optional[str] = None,
    end: str = "",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    text_to_print = get_colored_text(text, color) if color else text
    print(text_to_print, end=end, file=file, flush=flush)
    if file:
        file.flush()