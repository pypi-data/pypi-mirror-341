# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

github_dark_tritanopia: Dict[str, Any] = loads(s = """\
    # (Github Dark Tritanopia) Colors for Alacritty

    # Default colors
    [colors.primary]
    background = '#0d1117'
    foreground = '#c9d1d9'

    # Cursor colors
    [colors.cursor]
    text = '#0d1117'
    cursor = '#c9d1d9'

    # Normal colors
    [colors.normal]
    black = '#484f58'
    red = '#ff7b72'
    green = '#58a6ff'
    yellow = '#d29922'
    blue = '#58a6ff'
    magenta = '#bc8cff'
    cyan = '#39c5cf'
    white = '#b1bac4'

    # Bright colors
    [colors.bright]
    black = '#6e7681'
    red = '#ffa198'
    green = '#79c0ff'
    yellow = '#e3b341'
    blue = '#79c0ff'
    magenta = '#bc8cff'
    cyan = '#39c5cf'
    white = '#b1bac4'
    """
)