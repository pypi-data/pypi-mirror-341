#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper
from typing import Any, Dict, List

from toml import dump, load

from config.path import alacritty_toml_path
from lib.format_ansi_color import bold, italic


# Change Font -> Abbreviated cf
async def change_font(*, font_name: str, lista: List[str]) -> None:
    """
    Updates the font configuration in the Alacritty configuration file.

    This function modifies the font settings in the `alacritty.toml` file, allowing customization of the font used in the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `font_name (str)`: The new font name.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is enabled.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the font family (`family`) value in the configuration.
    3. Adds default keys if they do not exist in the configuration.
    4. Writes the changes back to the configuration file.
    5. Adds the font command to the command list for verbose output.

    Returns:
    - `None`
    """
    f: TextIOWrapper
    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        new_font_data: Dict[str, Any] = load(f=f)

    _keys: Dict[str, Any] = new_font_data.get("font", dict())

    if "normal" not in _keys:
        new_font_data["font"]["normal"] = dict(family=font_name, style="Regular")

    _keys = _keys.get("normal", dict())
    if "family" not in _keys:
        new_font_data["font"]["normal"]["family"] = font_name

    if "family" in _keys:
        new_font_data["font"]["normal"]["family"] = font_name

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=new_font_data, f=f)

    # Add the key to the command list for verbose output
    lista.append(
        bold(text="Font: ", color="green") + italic(text=font_name, color="cyan")
    )
    return None
