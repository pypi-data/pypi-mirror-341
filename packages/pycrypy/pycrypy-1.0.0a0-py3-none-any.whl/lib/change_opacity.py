#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper
from typing import Any, Dict, List

from toml import dump, load

from config.path import alacritty_toml_path
from lib.alacritty_key import window_key
from lib.format_ansi_color import bold, italic


# Change Opacity -> Abbreviated co
async def change_opacity(*, opacity: float, lista: List[str]) -> None:
    """
    Changes the window opacity in the Alacritty configuration file.

    This function updates the window opacity in the `alacritty.toml` file, allowing customization of the transparency of the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `opacity (float)`: The new opacity level of the window (value between 0.0 and 1.0).
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the `opacity` value in the configuration.
    3. Adds default keys if they do not exist in the configuration, including `startup_mode` and `padding`.
    4. Writes the changes back to the configuration file.
    5. Adds the opacity command to the list of commands for verbose output.

    Returns:
    - `None`
    """
    f: TextIOWrapper

    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        current_opacity_data: Dict[str, Any] = load(f=f)
    window_key["window"]["opacity"] = opacity

    # Verify if the "window" key exists, otherwise create it with default values
    if "window" not in current_opacity_data:
        current_opacity_data.update(window_key)

    _keys: Dict[str, Any] = current_opacity_data.get("window", dict())

    if "opacity" not in _keys:
        current_opacity_data["window"]["opacity"] = opacity
    else:
        current_opacity_data["window"]["opacity"] = opacity
    if "startup_mode" not in _keys:
        current_opacity_data["window"]["startup_mode"] = "Maximized"
    if "padding" not in _keys:
        current_opacity_data["window"]["padding"] = dict(x=5, y=5)

    _keys = _keys.get("padding", dict())

    if "x" not in _keys:
        current_opacity_data["window"]["padding"]["x"] = 5
    if "y" not in _keys:
        current_opacity_data["window"]["padding"]["y"] = 5

    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=current_opacity_data, f=f)

    # Add the key to the command list for verbose output
    lista.append(
        bold(text="Opacity: ", color="green") + italic(text=str(opacity), color="yellow")
    )
    return None
