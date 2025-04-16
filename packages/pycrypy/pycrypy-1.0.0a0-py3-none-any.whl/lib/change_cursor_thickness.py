#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper
from typing import Any, Dict, List

from toml import dump, load

from config.path import alacritty_toml_path
from lib.alacritty_key import cursor_key
from lib.format_ansi_color import bold, italic


# Change cursor thickness -> Abbreviated: cct
async def change_cursor_thickness(*, cursor_thickness: float, lista: List[str]) -> None:
    """
    Updates the cursor thickness configuration in the Alacritty configuration file.

    This function modifies the cursor thickness setting in the `alacritty.toml` file, allowing customization of how the cursor thickness is displayed in the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `cursor_thickness (float)`: The new cursor thickness value.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is enabled.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the cursor thickness (`thickness`) value in the configuration.
    3. Adds default keys if they do not exist in the configuration.
    4. Writes the changes back to the configuration file.
    5. Adds the cursor thickness command to the command list for verbose output.

    Returns:
    - `None`
    """
    f: TextIOWrapper

    data_cursor_thickness: Dict[str, Any]
    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        data_cursor_thickness = load(f=f)

    cursor_key["cursor"]["style"]["thickness"] = cursor_thickness

    if "cursor" not in data_cursor_thickness:
        data_cursor_thickness.update(cursor_key)

    _keys: Dict[str, Any] = data_cursor_thickness.get("cursor", dict())

    if "thickness" not in _keys:
        data_cursor_thickness["cursor"] = dict(thickness=cursor_thickness, style=dict())
    else:
        data_cursor_thickness["cursor"]["thickness"] = cursor_thickness

    if "style" not in _keys:
        data_cursor_thickness["cursor"]["style"] = dict(
            shape=cursor_thickness, blinking="off"
        )

    _keys = _keys.get("style", dict())

    if "blinking" not in _keys:
        data_cursor_thickness["cursor"]["style"] = dict(blinking="off")

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=data_cursor_thickness, f=f)

    # Add the key to the command list for verbose output
    lista.append(
        bold(text="Thickness: ", color="green")
        + italic(text=str(cursor_thickness), color="yellow")
    )
    return None
