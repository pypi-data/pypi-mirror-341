#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from sys import stdout
from typing import Dict

from colored import Fore, Style  # type: ignore

color_dict: Dict[str, str] = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
}


def bold(*, text: str = "", color: str) -> str:
    """
    ### This function returns a string with the text in bold and the specified color
    - Available colors: `black`, `red`, `green`, `yellow`, `blue`, `cyan`, `white`
    - Example:

    ```python
    bold(text="Hello world", color="green")
    ```
    """
    color = color_dict.get(color) or "black"
    color = Style.bold + color
    return color + f"{text}" + Style.reset


def italic(*, text: str = "", color: str) -> str:
    """
    ### This function returns a string with the text in italics and the specified color
    - Available colors: `black`, `red`, `green`, `yellow`, `blue`, `cyan`, `white`
    - Example:

    ```python
    italic(text="Hello world", color="green")
    ```
    """
    color = color_dict.get(color) or "black"
    color = Style.italic + color
    return color + f"{text}" + Style.reset


def underline(*, text: str = "", color: str) -> str:
    """
    ### This function returns a string with the text underlined and the specified color
    - Available colors: `black`, `red`, `green`, `yellow`, `blue`, `cyan`, `white`
    - Example:

    ```python
    underline(text="Hello world", color="green")
    ```
    """
    color = color_dict.get(color) or "black"
    color = Style.underline + color
    return color + f"{text}" + Style.reset


if __name__ == "__main__":
    print(bold(text="Hello world", color="green"), end="\n", flush=True, file=stdout)
    print(italic(text="Hello world", color="green"), end="\n", flush=True, file=stdout)
    print(
        underline(text="Hello world", color="green"), end="\n", flush=True, file=stdout
    )
