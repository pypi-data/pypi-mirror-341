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


# Cambiar Curso Shap -> Abreviado: ccs
async def change_cursor_shape(*, shape_name: str, lista: List[str]) -> None:
    """
    Changes the cursor shape configuration in the Alacritty configuration file.

    This function updates the cursor shape configuration in the `alacritty.toml` file, allowing customization of how the cursor is displayed in the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `shape_name (str)`: The new value for the cursor shape.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the cursor shape (`shape`) value in the configuration.
    3. Adds default keys if they do not exist in the configuration.
    4. Writes the changes back to the configuration file.
    5. Adds the cursor shape command to the list of commands for verbose output.

    Returns:
    - `None`
    """
    f: TextIOWrapper
    cursor_shape_data: Dict[str, Any]
    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        cursor_shape_data = load(f=f)

    cursor_key["cursor"]["style"]["shape"] = shape_name

    if "cursor" not in cursor_shape_data:
        cursor_shape_data.update(cursor_key)

    _keys: Dict[str, Any] = cursor_shape_data.get("cursor", dict())

    if "thickness" not in _keys:
        cursor_shape_data["cursor"] = {
            "thickness": 0.15,
            "style": {"shape": shape_name, "blinking": "off"},
        }

    if "style" not in _keys:
        cursor_shape_data["cursor"]["style"].update(
            dict(shape=shape_name, blinking="off")
        )

    if "blinking" not in _keys.get("style", dict()):
        cursor_shape_data["cursor"]["style"] = dict(blinking="off")

    cursor_shape_data["cursor"]["style"]["shape"] = shape_name

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=cursor_shape_data, f=f)

    # Add the key to the list of commands to display in the terminal if the -v flag is activated
    lista.append(
        bold(text="Shape: ", color="green") + italic(text=shape_name, color="cyan")
    )
    return None
