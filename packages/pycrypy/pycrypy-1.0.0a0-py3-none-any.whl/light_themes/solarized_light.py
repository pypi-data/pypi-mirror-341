# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

solarized_light: Dict[str, Any] = loads(s = """\
    # Colors (Solarized Light)

    # Default colors
    [colors.primary]
    background = '#fdf6e3'
    foreground = '#586e75'

    # Normal colors
    [colors.normal]
    black   = '#073642'
    red     = '#dc322f'
    green   = '#859900'
    yellow  = '#b58900'
    blue    = '#268bd2'
    magenta = '#d33682'
    cyan    = '#2aa198'
    white   = '#eee8d5'

    # Bright colors
    [colors.bright]
    black   = '#002b36'
    red     = '#cb4b16'
    green   = '#586e75'
    yellow  = '#657b83'
    blue    = '#839496'
    magenta = '#6c71c4'
    cyan    = '#93a1a1'
    white   = '#fdf6e3'
    """
)