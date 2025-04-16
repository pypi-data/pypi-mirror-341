# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

blood_moon: Dict[str, Any] = loads(s = """\
    # Colors (Blood Moon)

    # Default colors
    [colors.primary]
    background = '#10100E'
    foreground = '#C6C6C4'

    # Normal colors
    [colors.normal]
    black   = '#10100E'
    red     = '#C40233'
    green   = '#009F6B'
    yellow  = '#FFD700'
    blue    = '#0087BD'
    magenta = '#9A4EAE'
    cyan    = '#20B2AA'
    white   = '#C6C6C4'

    # Bright colors
    [colors.bright]
    black   = '#696969'
    red     = '#FF2400'
    green   = '#03C03C'
    yellow  = '#FDFF00'
    blue    = '#007FFF'
    magenta = '#FF1493'
    cyan    = '#00CCCC'
    white   = '#FFFAFA'
    """
)