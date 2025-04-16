# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

xterm: Dict[str, Any] = loads(s = """\
    # XTerm's default colors

    # Default colors
    [colors.primary]
    background = '#000000'
    foreground = '#ffffff'

    # Normal colors
    [colors.normal]
    black   = '#000000'
    red     = '#cd0000'
    green   = '#00cd00'
    yellow  = '#cdcd00'
    blue    = '#0000ee'
    magenta = '#cd00cd'
    cyan    = '#00cdcd'
    white   = '#e5e5e5'

    # Bright colors
    [colors.bright]
    black   = '#7f7f7f'
    red     = '#ff0000'
    green   = '#00ff00'
    yellow  = '#ffff00'
    blue    = '#5c5cff'
    magenta = '#ff00ff'
    cyan    = '#00ffff'
    white   = '#ffffff'
    """
)