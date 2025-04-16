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


# Change padding -> Abbreviated: cp
async def change_padding(*, padding_list: List[int], lista: List[str]) -> None:
    """
    Changes the padding of the window in the Alacritty configuration file.

    This function updates the padding values in the `alacritty.toml` file, allowing customization of the space between the window content and its borders in the Alacritty terminal emulator. If certain keys do not exist in the configuration, the function adds them with default values.

    Parameters:
    - `padding_list (List[int])`: A list with two integer values representing the padding on the x and y axes, respectively.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Reads the `alacritty.toml` configuration file.
    2. Updates the padding values (`padding.x` and `padding.y`) in the configuration.
    3. Adds default keys if they do not exist in the configuration, including `opacity` and `startup_mode`.
    4. Writes the changes back to the configuration file.
    5. Adds the padding command to the list of commands for verbose output.

    Returns:
    - `None`
    """
    f: TextIOWrapper

    with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
        current_padding_data: Dict[str, Any] = load(f=f)
    window_key["window"]["padding"]["x"], window_key["window"]["padding"]["y"] = (
        padding_list
    )

    # Verify if the "window" key exists, otherwise create it with default values
    if "window" not in current_padding_data:
        current_padding_data.update(window_key)

    _keys: Dict[str, Any] = current_padding_data.get("window", dict())

    if "opacity" not in _keys:
        current_padding_data["window"]["opacity"] = 0.9
    if "startup_mode" not in _keys:
        current_padding_data["window"]["startup_mode"] = "Maximized"
    if "padding" not in _keys:
        current_padding_data["window"]["padding"] = dict(
            x=padding_list[0], y=padding_list[1]
        )

    _keys = _keys.get("padding", dict())
    if "x" not in _keys:
        current_padding_data["window"]["padding"]["x"] = padding_list[0]
    else:
        current_padding_data["window"]["padding"]["x"] = padding_list[0]

    if "y" not in _keys:
        current_padding_data["window"]["padding"]["y"] = padding_list[1]
    else:
        current_padding_data["window"]["padding"]["y"] = padding_list[1]

    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=current_padding_data, f=f)

    # Add the key to the list of commands to display in the terminal if the -v flag is activated
    lista.append(
        bold(text="Padding: ", color="green")
        + bold(text="[ ", color="cyan")
        + italic(text=", ".join(map(lambda i: str(i), padding_list)), color="yellow")
        + bold(text=" ]", color="cyan")
    )
    return None
