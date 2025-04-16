# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

dark_pastels: Dict[str, Any] = loads(s = """\
    # Colors (Konsole's Dark Pastels)

    # Default colors
    [colors.primary]
    background = '#2C2C2C'
    foreground = '#DCDCCC'

    # Normal colors
    [colors.normal]
    black   = '#3F3F3F'
    red     = '#705050'
    green   = '#60B48A'
    yellow  = '#DFAF8F'
    blue    = '#9AB8D7'
    magenta = '#DC8CC3'
    cyan    = '#8CD0D3'
    white   = '#DCDCCC'

    # Bright colors
    [colors.bright]
    black   = '#709080'
    red     = '#DCA3A3'
    green   = '#72D5A3'
    yellow  = '#F0DFAF'
    blue    = '#94BFF3'
    magenta = '#EC93D3'
    cyan    = '#93E0E3'
    white   = '#FFFFFF'
    """
)