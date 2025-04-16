#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper
from sys import stderr
from types import ModuleType
from typing import Any, Dict, List, Optional

from toml import TomlDecodeError, dump, load

from config.errors import topic_not_found
from config.path import alacritty_toml_path
from config.themes import (  # light_themes, dark_themes, recommended_themes
    dark_themes,
    light_themes,
    load_themes,
    recommended_themes,
)
from lib.alacritty_key import *  # noqa: F403
from lib.alacritty_key import cursor_key, font_key, window_key
from lib.format_ansi_color import bold, italic


# region Cargar Tema
# Load New Theme -> Abbreviated lnt
async def load_new_theme(*, new_alacritty_theme: str, lista: List[str]) -> None:
    """
    Loads a new configuration theme for Alacritty from a specified theme module.

    This function searches for a specific theme in the available theme modules (`light_themes`, `dark_themes`, `recommended_themes`). If the theme is found, it loads the theme configuration into the Alacritty terminal. If the current configuration file has formatting issues, the function handles and corrects it if necessary.

    Parameters:
    - `new_alacritty_theme (str)`: The name of the new theme to be loaded.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Dynamically loads themes from the `light_themes`, `dark_themes`, and `recommended_themes` modules.
    2. Checks if the specified theme (`new_alacritty_theme`) exists in the loaded theme modules.
    3. Dynamically imports the theme module from the corresponding dictionary and retrieves the theme configuration.
    4. If the theme is not found in any module, prints an error message and terminates execution.
    5. Attempts to read the Alacritty configuration file (`alacritty_toml_path`). If the file has incorrect formatting, it overwrites it with an empty file and rereads it.
    6. Calls the `sta` function to apply the new theme to the current Alacritty configuration.
    7. Adds an error message to the command list if the Alacritty configuration file had formatting issues.

    Returns:
    - `None`
    """
    light_themes_dict: Dict[str, Any] = dict()
    dark_themes_dict: Dict[str, Any] = dict()
    recommended_themes_dict: Dict[str, Any] = dict()

    theme_exists: bool = False
    theme_module: Optional[ModuleType] = None
    new_theme_data: Dict[str, Any] = dict()

    # Check if the module is in the dictionary
    if new_alacritty_theme in recommended_themes:
        recommended_themes_dict.update(
            await load_themes(
                base_module="recommended_themes", theme_name=new_alacritty_theme
            )
        )

        # Dynamically import the module from the dictionary
        theme_module = recommended_themes_dict[new_alacritty_theme]

        # Assume `new_alacritty_theme` is a variable within the module
        if hasattr(theme_module, new_alacritty_theme):
            new_theme_data = getattr(theme_module, new_alacritty_theme)
            theme_exists = True
        else:
            print(
                f"Variable {new_alacritty_theme} not found in module {new_alacritty_theme}",
                file=stderr,
            )

    # Check if the module is in the dictionary
    if not theme_exists and new_alacritty_theme in light_themes:
        light_themes_dict.update(
            await load_themes(
                base_module="light_themes", theme_name=new_alacritty_theme
            )
        )

        # Dynamically import the module from the dictionary
        theme_module = light_themes_dict[new_alacritty_theme]

        # Assume `new_alacritty_theme` is a variable within the module
        if hasattr(theme_module, new_alacritty_theme):
            new_theme_data = getattr(theme_module, new_alacritty_theme)
            theme_exists = True
        else:
            print(
                f"Variable {new_alacritty_theme} not found in module {new_alacritty_theme}",
                file=stderr,
            )

    # Check if the module is in the dictionary
    if not theme_exists and new_alacritty_theme in dark_themes:
        dark_themes_dict.update(
            await load_themes(base_module="dark_themes", theme_name=new_alacritty_theme)
        )

        # Dynamically import the module from the dictionary
        theme_module = dark_themes_dict[new_alacritty_theme]

        # Assume `new_alacritty_theme` is a variable within the module
        if hasattr(theme_module, new_alacritty_theme):
            new_theme_data = getattr(theme_module, new_alacritty_theme)
            theme_exists = True
        else:
            print(
                f"Variable {new_alacritty_theme} not found in module {new_alacritty_theme}",
                end="\n",
                file=stderr,
            )

    if not theme_exists:
        print(
            await topic_not_found(name_topic=new_alacritty_theme),
            end="\n",
            flush=True,
            file=stderr,
        )
        exit(code=1)

    e: TomlDecodeError
    f: TextIOWrapper
    # Load the current theme used by the Alacritty terminal
    try:
        with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
            current_theme_data: Dict[str, Any] = load(f=f)
    except TomlDecodeError as e:
        print(
            bold(
                text=f"Error: The file format is incorrect and will be overwritten `{e}`.",
                color="red",
            ),
            end="\n",
            flush=True,
            file=stderr,
        )
        with open(file=alacritty_toml_path, mode="w") as f:
            f.write("")
        with open(file=alacritty_toml_path, mode="r", encoding="utf-8") as f:
            current_theme_data = load(f=f)
        # Add the key to the command list to display in the terminal if the -v flag is activated
        lista.append(
            bold(
                text="The file format is incorrect and will be overwritten `{e}`.",
                color="red",
            )
        )

    await overwrite_theme(
        alacritty_toml_path=alacritty_toml_path,
        new_theme_data=new_theme_data,
        current_theme_data=current_theme_data,
        new_alacritty_theme=new_alacritty_theme,
        lista=lista,
    )

    return None


# region Cambiar Tema
# Funcion que cambia el tema de alacritty
# SobreEscribir Tema -> Abreviado: sta
async def overwrite_theme(
    alacritty_toml_path: str,
    new_theme_data: Dict[str, Any],
    current_theme_data: Dict[str, Any],
    new_alacritty_theme: str,
    lista: List[str],
) -> None:
    """
    Overwrites the theme configuration in the Alacritty configuration file.

    This function updates the current Alacritty configuration with the values of the specified new theme. If any required key is missing in the current configuration, it creates them with default values. Finally, it saves the updated configuration to the Alacritty configuration file.

    Parameters:
    - `alacritty_toml_path (str)`: The path to the Alacritty configuration file to be updated.
    - `new_theme_data (Dict[str, Any])`: The configuration of the new theme to be applied.
    - `current_theme_data (Dict[str, Any])`: The current Alacritty configuration to be updated.
    - `new_alacritty_theme (str)`: The name of the new theme to be applied.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Checks if the new theme file contains the `colors` key. If not, prints an error message and terminates execution.
    2. Updates the current configuration with the colors of the new theme.
    3. Validates and ensures that the required keys (`font`, `window`, `cursor`) are present in the current configuration, creating them with default values if missing.
    4. Overwrites the Alacritty configuration file with the updated configuration.
    5. Adds a message to the command list if the -v flag is activated, indicating that the new theme has been applied.

    Returns:
    - `None`
    """

    if "colors" not in new_theme_data:
        print(
            bold(text="Error: The content of the file is not valid", color="red"),
            flush=True,
            file=stderr,
            end="\n",
        )
        exit(code=1)

    # Create the "colors" key
    current_theme_data["colors"] = new_theme_data["colors"]

    # * Validate that all fields exist, and if not, create the keys with default values
    if "font" not in current_theme_data:
        current_theme_data.update(font_key)

    _keys: Dict[str, Any] = current_theme_data.get("font", dict())

    if "size" not in current_theme_data.get("font", dict()):
        current_theme_data["font"] = {"size": 11.25, "normal": dict()}

    if "normal" not in current_theme_data["font"]:
        current_theme_data["font"]["normal"] = dict(
            family="monospace",
            style="Regular",
        )

    _keys = _keys.get("normal", dict())

    if "family" not in _keys:
        current_theme_data["font"]["normal"]["family"] = "monospace"

    if "style" not in _keys:
        current_theme_data["font"]["normal"]["style"] = "Regular"
    if "offset" not in _keys:
        current_theme_data["font"]["offset"] = dict(x=0, y=0)
    if "x" not in current_theme_data["font"]["offset"]:
        current_theme_data["font"]["offset"]["x"] = 0
    if "y" not in current_theme_data["font"]["offset"]:
        current_theme_data["font"]["offset"]["y"] = 0

    # Verify if the "window" key exists, if not, create the key with default values
    if "window" not in current_theme_data:
        current_theme_data.update(window_key)

    _keys = current_theme_data.get("window", dict())
    if "opacity" not in _keys:
        current_theme_data["window"]["opacity"] = 0.9

    if "startup_mode" not in _keys:
        current_theme_data["window"]["startup_mode"] = "Maximized"

    if "padding" not in _keys:
        current_theme_data["window"]["padding"] = dict(x=5, y=5)

    if "x" not in current_theme_data["window"]["padding"]:
        current_theme_data["window"]["padding"]["x"] = 5

    if "y" not in current_theme_data["window"]["padding"]:
        current_theme_data["window"]["padding"]["y"] = 5

    # Verify if the "cursor" key exists, if not, create the key with default values
    if "cursor" not in current_theme_data:
        current_theme_data.update(cursor_key)

    _keys = current_theme_data.get("cursor", dict())
    if "thickness" not in _keys:
        current_theme_data["cursor"]["thickness"] = 0.15

    if "style" not in _keys:
        current_theme_data["cursor"]["style"] = dict(shape="Block", blinking="off")

    if "shape" not in current_theme_data["cursor"]["style"]:
        current_theme_data["cursor"]["style"]["shape"] = "Block"

    if "blinking" not in current_theme_data["cursor"]["style"]:
        current_theme_data["cursor"]["style"]["blinking"] = "off"

    # Swap the theme values
    new_theme_data = current_theme_data

    # Overwrite the file
    with open(file=alacritty_toml_path, mode="w") as f:
        dump(o=new_theme_data, f=f)

    # Add the key to the command list to display in the terminal if the -v flag is activated
    lista.append(
        bold(text="Theme: ", color="green")
        + italic(text=new_alacritty_theme, color="cyan")
    )
    return None


# endregion
