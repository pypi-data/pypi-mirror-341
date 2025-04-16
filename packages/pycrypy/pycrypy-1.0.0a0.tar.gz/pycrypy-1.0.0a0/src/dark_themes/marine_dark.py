# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

marine_dark: Dict[str, Any] = loads(s = """\
    # Marine Dark Theme
    # Source https//github.com/ProDeSquare/alacritty-colorschemes/blob/master/themes/marine_dark.yaml

    # Default colors
    [colors.primary]
    background = '#002221'
    foreground = '#e6f8f8'

    # Normal colors
    [colors.normal]
    black   = '#002221'
    red     = '#ea3431'
    green   = '#00b6b6'
    yellow  = '#f8b017'
    blue    = '#4894fd'
    magenta = '#e01dca'
    cyan    = '#1ab2ad'
    white   = '#99dddb'

    # Bright colors
    [colors.bright]
    black   = '#006562'
    red     = '#ea3431'
    green   = '#00b6b6'
    yellow  = '#f8b017'
    blue    = '#4894fd'
    magenta = '#e01dca'
    cyan    = '#1ab2ad'
    white   = '#e6f6f6'
    """
)