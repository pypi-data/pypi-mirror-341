# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

snazzy: Dict[str, Any] = loads(s = """\
    # Colors (Snazzy)

    # Default colors
    [colors.primary]
    background = '#282a36'
    foreground = '#eff0eb'

    # Normal colors
    [colors.normal]
    black   = '#282a36'
    red     = '#ff5c57'
    green   = '#5af78e'
    yellow  = '#f3f99d'
    blue    = '#57c7ff'
    magenta = '#ff6ac1'
    cyan    = '#9aedfe'
    white   = '#f1f1f0'

    # Bright colors
    [colors.bright]
    black   = '#686868'
    red     = '#ff5c57'
    green   = '#5af78e'
    yellow  = '#f3f99d'
    blue    = '#57c7ff'
    magenta = '#ff6ac1'
    cyan    = '#9aedfe'
    white   = '#f1f1f0'
    """
)