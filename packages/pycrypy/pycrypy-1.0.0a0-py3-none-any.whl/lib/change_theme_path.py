#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper
from sys import stderr
from typing import Any, Dict, List, NoReturn, Union

from toml import TomlDecodeError, load

from config.path import alacritty_toml_path
from lib.format_ansi_color import bold
from lib.load_new_theme import (
    overwrite_theme,  # sta -> sobreescribir tema actual -> Abreviado: sta
)


# Change Theme Path -> Abbreviated: ctp
async def change_theme_path(
    *, theme_path: str, lista: List[str]
) -> Union[None, NoReturn]:
    """
    Changes the Alacritty configuration theme from a specified theme file.

    This function replaces the current Alacritty theme with a new one loaded from a theme configuration file (`theme_path`). If the new theme file or the Alacritty configuration file has formatting issues, the function handles the errors and takes measures to correct the configuration file.

    Parameters:
    - `theme_path (str)`: The path to the theme file to be applied.
    - `lista (List[str])`: A list of commands to display in the terminal if the -v flag is activated.

    Actions:
    1. Attempts to read the new theme file (`theme_path`). If an error occurs while reading the file (such as incorrect format or file not found), prints an error message and exits the program.
    2. Attempts to read the Alacritty configuration file (`alacritty_toml_path`). If the file has an incorrect format, it overwrites it with an empty file and re-reads it.
    3. Calls the `overwrite_theme` function to apply the new theme to the current Alacritty configuration.
    4. Adds an error message to the command list if the Alacritty configuration file had formatting issues.

    Returns:
    - `None`
    """
    e: Union[TomlDecodeError, FileNotFoundError]
    f: TextIOWrapper
    try:
        with open(file=theme_path, mode="r") as f:
            new_theme_data: Dict[str, Any] = load(f=f)
    except (TomlDecodeError, FileNotFoundError) as e:
        print(
            bold(text=f"Error: `{e}`.", color="red"), end="\n", flush=True, file=stderr
        )
        print(
            bold(
                text=f"Error: Verify if the format of the file `{theme_path}` is correct or if the file path is correct.",
                color="green",
            ),
            end="\n",
            flush=True,
            file=stderr,
        )
        exit(code=1)

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
        new_alacritty_theme=theme_path,
        lista=lista,
    )

    return None
