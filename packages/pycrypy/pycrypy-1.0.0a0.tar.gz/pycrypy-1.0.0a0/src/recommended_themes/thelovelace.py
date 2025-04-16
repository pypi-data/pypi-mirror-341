# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

thelovelace: Dict[str, Any] = loads(s = """\
    # Default colors
    [colors.primary]
    background = '#1D1F28'
    foreground = '#FDFDFD'

    # Normal colors
    [colors.normal]
    # Bright colors
    black   = '#282A36'
    red     = '#F37F97'
    green   = '#5ADECD'
    yellow  = '#F2A272'
    blue    = '#8897F4'
    magenta = '#C574DD'
    cyan    = '#79E6F3'
    white   = '#FDFDFD'

    [colors.bright]
    black   = '#414458'
    red     = '#FF4971'
    green   = '#18E3C8'
    yellow  = '#EBCB8B'
    blue    = '#FF8037'
    magenta = '#556FFF'
    cyan    = '#3FDCEE'
    white   = '#BEBEC1'
    """
)