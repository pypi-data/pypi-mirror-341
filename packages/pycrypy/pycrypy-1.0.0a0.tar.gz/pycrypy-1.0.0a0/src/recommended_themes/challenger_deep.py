# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

challenger_deep: Dict[str, Any] = loads(s = """\
    # Colors (Challenger Deep)

    # Default colors
    [colors.primary]
    background = '#1e1c31'
    foreground = '#cbe1e7'

    [colors.cursor]
    text = '#ff271d'
    cursor = '#fbfcfc'

    # Normal colors
    [colors.normal]
    black   = '#141228'
    red     = '#ff5458'
    green   = '#62d196'
    yellow  = '#ffb378'
    blue    = '#65b2ff'
    magenta = '#906cff'
    cyan    = '#63f2f1'
    white   = '#a6b3cc'

    # Bright colors
    [colors.bright]
    black   = '#565575'
    red     = '#ff8080'
    green   = '#95ffa4'
    yellow  = '#ffe9aa'
    blue    = '#91ddff'
    magenta = '#c991e1'
    cyan    = '#aaffe4'
    white   = '#cbe3e7'
    """
)