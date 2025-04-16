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


# Change Cursor Blinking -> Abbreviation: ccb
async def change_cursor_blinking(*, blinking_name: str, lista: List[str]) -> None:
    """
    Changes the cursor blinking setting in the Alacritty configuration file.

    This function updates the cursor blinking behavior in the `alacritty.toml` file,
    allowing customization of how the cursor blinks in the Alacritty terminal emulator.
    If certain keys do not exist in the configuration, the function adds them with default values.

    Args:
        blinking_name (str): The new blinking value for the cursor.
        lista (List[str]): A list of commands to be shown in the terminal when the -v flag is active.

    Actions:
        1. Reads the `alacritty.toml` configuration file.
        2. Updates the `blinking` value under the cursor settings.
        3. Adds default keys if they do not exist in the configuration.
        4. Writes the changes back to the configuration file.
        5. Appends the blinking change command to the list for verbose output.

    Returns:
        None
    """
    f: TextIOWrapper
    cursor_data: Dict[str, Any]
    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        cursor_data = load(f=f)

    cursor_key["cursor"]["style"]["blinking"] = blinking_name

    if "cursor" not in cursor_data:
        cursor_data.update(cursor_key)

    _keys: Dict[str, Any] = cursor_data.get("cursor", dict())

    if "thickness" not in _keys or not isinstance(cursor_data["cursor"], dict):
        cursor_data["cursor"] = dict(thickness=0.15, style={})

    if "style" not in _keys:
        cursor_data["cursor"]["style"] = dict(shape="Block", blinking=blinking_name)

    _keys = _keys.get("style", dict())

    if "shape" not in _keys:
        cursor_data["cursor"]["style"] = dict(shape="Block")

    _keys = cursor_data.get("cursor", dict())

    if "style" not in _keys or not isinstance(cursor_data["cursor"]["style"], dict):
        cursor_data["cursor"]["style"] = dict()

    cursor_data["cursor"]["style"]["blinking"] = blinking_name

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=cursor_data, f=f)

    # Add the command to the list if -v flag is active
    lista.append(
        bold(text="Blinking: ", color="green")
        + italic(text=blinking_name, color="cyan")
    )
    return None
