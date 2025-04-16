#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper
from typing import Any, Dict, List

from toml import dump, load

from config.path import alacritty_toml_path
from lib.alacritty_key import font
from lib.format_ansi_color import bold, italic


# Change Font Style -> Abbreviated cfs
async def change_font_style(*, font_style: str, lista: List[str]) -> None:
    """
    Updates the font style configuration in the Alacritty configuration file.

    This function modifies the font style setting in the `alacritty.toml` file, allowing customization of how the font style is displayed in the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `font_style (str)`: The new font style value.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is enabled.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the font style (`style`) value in the configuration.
    3. Adds default keys if they do not exist in the configuration.
    4. Writes the changes back to the configuration file.
    5. Adds the font style command to the command list for verbose output.

    Returns:
    - `None`
    """

    f: TextIOWrapper
    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        font_style_data: Dict[str, Any] = load(f=f)

    _keys: Dict[str, Any] = font_style_data.get("font", dict())

    if "normal" not in _keys:
        font_style_data["font"]["normal"] = dict(family=font, style=font_style)

    _keys = _keys.get("normal", dict())

    if "style" not in _keys:
        font_style_data["font"]["normal"]["style"] = font_style

    if "style" in _keys:
        font_style_data["font"]["normal"]["style"] = font_style

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=font_style_data, f=f)

    # Add the key to the command list for verbose output if the -v flag is enabled
    lista.append(
        bold(text="Style: ", color="green") + italic(text=font_style, color="cyan")
    )
    return None
