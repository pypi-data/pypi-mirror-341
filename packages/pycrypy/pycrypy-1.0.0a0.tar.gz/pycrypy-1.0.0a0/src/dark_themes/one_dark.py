# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

one_dark: Dict[str, Any] = loads(s = """\
    # Colors (One Dark)

    # Default colors
    [colors.primary]
    background = '#282c34'
    foreground = '#abb2bf'

    # Normal colors
    [colors.normal]
    black   = '#1e2127'
    red     = '#e06c75'
    green   = '#98c379'
    yellow  = '#d19a66'
    blue    = '#61afef'
    magenta = '#c678dd'
    cyan    = '#56b6c2'
    white   = '#abb2bf'

    # Bright colors
    [colors.bright]
    black   = '#5c6370'
    red     = '#e06c75'
    green   = '#98c379'
    yellow  = '#d19a66'
    blue    = '#61afef'
    magenta = '#c678dd'
    cyan    = '#56b6c2'
    white   = '#ffffff'
    """
)