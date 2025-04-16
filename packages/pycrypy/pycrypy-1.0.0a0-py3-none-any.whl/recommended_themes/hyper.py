# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

hyper: Dict[str, Any] = loads(s = """\
    # Colors (Hyper)

    # Default colors
    [colors.primary]
    background = '#000000'
    foreground = '#ffffff'

    [colors.cursor]
    text = '#F81CE5'
    cursor = '#ffffff'

    # Normal colors
    [colors.normal]
    black   = '#000000'
    red     = '#fe0100'
    green   = '#33ff00'
    yellow  = '#feff00'
    blue    = '#0066ff'
    magenta = '#cc00ff'
    cyan    = '#00ffff'
    white   = '#d0d0d0'

    # Bright colors
    [colors.bright]
    black   = '#808080'
    red     = '#fe0100'
    green   = '#33ff00'
    yellow  = '#feff00'
    blue    = '#0066ff'
    magenta = '#cc00ff'
    cyan    = '#00ffff'
    white   = '#FFFFFF'
    """
)