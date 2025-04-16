# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

chicago95: Dict[str, Any] = loads(s = """\
    # Windows 95 Color Scheme
    # To have the authentic experience in Chicago95 GTK Theme.

    # Default colors
    [colors.primary]
    background = '#000000'
    foreground = '#C0C7C8'

    # Normal colors
    [colors.normal]
    black   = '#000000'
    red     = '#A80000'
    green   = '#00A800'
    yellow  = '#A85400'
    blue    = '#0000A8'
    magenta = '#A800A8'
    cyan    = '#00A8A8'
    white   = '#A8A8A8'

    # Bright colors
    [colors.bright]
    black   = '#545454'
    red     = '#FC5454'
    green   = '#54FC54'
    yellow  = '#FCFC54'
    blue    = '#5454FC'
    magenta = '#FC54FC'
    cyan    = '#54FCFC'
    white   = '#FFFFFF'
    """
)