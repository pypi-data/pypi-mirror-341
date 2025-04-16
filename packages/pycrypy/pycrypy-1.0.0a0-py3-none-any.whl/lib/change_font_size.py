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


# Change Font Size: Abbreviated -> cfs
async def change_font_size(*, font_size: float, lista: List[str]) -> None:
    """
    Changes the font size in the Alacritty configuration file.

    This function updates the font size in the `alacritty.toml` file, allowing customization of the text size in the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `font_size (float)`: The new font size to set.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the font size value (`font.size`) in the configuration.
    3. Adds default keys if they do not exist in the configuration, including `font.normal` and `font.offset`.
    4. Writes the changes back to the configuration file.
    5. Adds the font size command to the list of commands for verbose output.

    Returns:
    - `None`
    """
    f: TextIOWrapper
    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        font_size_data: Dict[str, Any] = load(f=f)
    if "normal" not in font_size_data["font"]:
        font_size_data["font"]["normal"] = dict(family=font, style="Regular")
    if "family" not in font_size_data["font"]["normal"]:
        font_size_data["font"]["normal"]["family"] = font
    if "offset" not in font_size_data["font"]:
        font_size_data["font"]["offset"] = dict(x=0, y=0)
    font_size_data["font"]["size"] = font_size

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=font_size_data, f=f)

    # Add the key to the command list for verbose output if the -v flag is activated
    lista.append(
        bold(text="Size Font: ", color="green")
        + italic(text=str(font_size), color="yellow")
    )
    return None
