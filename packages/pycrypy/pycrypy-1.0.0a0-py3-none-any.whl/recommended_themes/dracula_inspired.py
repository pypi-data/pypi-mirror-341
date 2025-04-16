# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

dracula_inspired: Dict[str, Any] = loads(s = """\
    # Themes Colors (dracula-inspired)

    # Default colors dracula-inspired

    [colors.primary]
    background = '0x292d3e'
    foreground = '0xbbc5ff'

    # Normal colors dracula-inspired
    [colors.normal]
    black = '#101010'
    red = '#f07178'
    green = '#c3e88d'
    yellow = '#ffcb6b'
    blue = '#82aaff'
    magenta = '#c792ea'
    cyan = '#89ddff'
    white = '#d0d0d0'

    # Bright colors dracula-inspired
    [colors.bright]
    black = '#434758'
    red = '#ff8b92'
    green = '#ddffa7'
    yellow = '#ffe585'
    blue = '#9cc4ff'
    magenta = '#e1acff'
    cyan = '#a3f7ff'
    white = '#ffffff'
    """
)