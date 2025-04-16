# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

iris: Dict[str, Any] = loads(s = """\
    # Colors (Iris)

    # Default colors
    [colors.primary]
    background = '#272537'
    foreground = '#e8e6e9'

    # Normal colors
    [colors.normal]
    black   = '#111133'
    red     = '#d61d52'
    green   = '#48a842'
    yellow  = '#e1a51c'
    blue    = '#5556d3'
    magenta = '#8650d3'
    cyan    = '#52afb7'
    white   = '#9f9aa7'

    # Bright colors
    [colors.bright]
    black   = '#484867'
    red     = '#e15877'
    green   = '#71ab3a'
    yellow  = '#c6a642'
    blue    = '#6d6dc9'
    magenta = '#956ad3'
    cyan    = '#6ab6bd'
    white   = '#e8e6e9'
    """
)