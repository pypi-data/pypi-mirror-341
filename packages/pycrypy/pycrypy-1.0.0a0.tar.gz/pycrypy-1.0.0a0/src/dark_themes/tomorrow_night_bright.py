# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

tomorrow_night_bright: Dict[str, Any] = loads(s = """\
    # Colors (Tomorrow Night Bright)

    # Default colors
    [colors.primary]
    background = '#000000'
    foreground = '#eaeaea'

    # Normal colors
    [colors.normal]
    black   = '#000000'
    red     = '#d54e53'
    green   = '#b9ca4a'
    yellow  = '#e6c547'
    blue    = '#7aa6da'
    magenta = '#c397d8'
    cyan    = '#70c0ba'
    white   = '#424242'

    # Bright colors
    [colors.bright]
    black   = '#666666'
    red     = '#ff3334'
    green   = '#9ec400'
    yellow  = '#e7c547'
    blue    = '#7aa6da'
    magenta = '#b77ee0'
    cyan    = '#54ced6'
    white   = '#2a2a2a'
    """
)