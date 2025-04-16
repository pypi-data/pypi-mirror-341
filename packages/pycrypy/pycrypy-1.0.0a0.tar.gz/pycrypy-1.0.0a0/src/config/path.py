#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from os.path import expanduser, join
from pathlib import Path
from typing import List

from lib.format_ansi_color import bold, italic

alacritty_toml_path: str = join(
    expanduser(path="~"), ".config", "alacritty", "alacritty.toml"
)

config_directory_path: str = join(expanduser(path="~"), ".config")
alacritty_directory_path: str = join(expanduser(path="~"), ".config", "alacritty")

# Verificar si el directorio existe el fichero alcritty.toml
# Verify If Directory Exists -> Abbreviated: vid
async def verify_if_directory_exists(lista: List[str]) -> None:
    config_path: Path = Path(config_directory_path)
    if not config_path.exists():
        config_path.mkdir(parents=True, exist_ok=True)
        lista.append(
            bold(text="Directory created: ", color="green")
            + italic(text=config_directory_path, color="cyan")
        )

    alacritty_path: Path = Path(alacritty_directory_path)

    if not alacritty_path.exists():
        alacritty_path.mkdir(parents=True, exist_ok=True)
        lista.append(
            bold(text="Directory created: ", color="green")
            + italic(text=alacritty_directory_path, color="cyan")
        )

    alacritty_toml: Path = Path(alacritty_toml_path)
    alacritty_toml.touch()
    lista.append(
        bold(text="File created: ", color="green")
        + italic(text=alacritty_toml_path, color="cyan")
    )
    return None

