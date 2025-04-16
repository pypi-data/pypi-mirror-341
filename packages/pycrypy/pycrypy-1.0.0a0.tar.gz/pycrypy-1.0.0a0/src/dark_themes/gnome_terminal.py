# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

gnome_terminal: Dict[str, Any] = loads(s = """\
    # Gnome (Gnome Terminal Default)

    # Default colors
    [colors.primary]
    background = '#1e1e1e'
    foreground = '#ffffff'

    # Normal colors
    [colors.normal]
    black      = '#171421'
    red        = '#c01c28'
    green      = '#26a269'
    yellow     = '#a2734c'
    blue       = '#12488b'
    magenta    = '#a347ba'
    cyan       = '#2aa1b3'
    white      = '#d0cfcc'

    # Bright colors
    [colors.bright]
    black      = '#5e5c64'
    red        = '#f66151'
    green      = '#33d17a'
    yellow     = '#e9ad0c'
    blue       = '#2a7bde'
    magenta    = '#c061cb'
    cyan       = '#33c7de'
    white      = '#ffffff'
    """
)