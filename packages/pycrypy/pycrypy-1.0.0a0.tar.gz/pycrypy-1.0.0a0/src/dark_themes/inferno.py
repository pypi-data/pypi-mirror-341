# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

inferno: Dict[str, Any] = loads(s = """\
    # Inferno theme
    # Source https//github.com/hafiz-muhammad/inferno-alacritty-theme

    # Default colors
    [colors.primary]
    background = '#270d06'
    foreground = '#d9d9d9'

    # Normal colors
    [colors.normal]
    black   = '#330000'
    red     = '#ff3300'
    green   = '#ff6600'
    yellow  = '#ff9900'
    blue    = '#ffcc00'
    magenta = '#ff6600'
    cyan    = '#ff9900'
    white   = '#d9d9d9'

    # Bright colors
    [colors.bright]
    black   = '#663300'
    red     = '#ff6633'
    green   = '#ff9966'
    yellow  = '#ffcc99'
    blue    = '#ffcc33'
    magenta = '#ff9966'
    cyan    = '#ffcc99'
    white   = '#d9d9d9'
    """
)