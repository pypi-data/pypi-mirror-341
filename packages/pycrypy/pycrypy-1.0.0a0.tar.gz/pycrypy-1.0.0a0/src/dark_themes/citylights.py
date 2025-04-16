# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

citylights: Dict[str, Any] = loads(s = """\
    # Default colors
    [colors.primary]
    background = '#171d23'
    foreground = '#ffffff'

    # Cursor colors
    [colors.cursor]
    text   = '#fafafa'
    cursor = '#008b94'

    # Normal colors
    [colors.normal]
    black   = '#333f4a'
    red     = '#d95468'
    green   = '#8bd49c'
    blue    = '#539afc'
    magenta = '#b62d65'
    cyan    = '#70e1e8'
    white   = '#b7c5d3'

    # Bright colors
    [colors.bright]
    black   = '#41505e'
    red     = '#d95468'
    green   = '#8bd49c'
    yellow  = '#ebbf83'
    blue    = '#5ec4ff'
    magenta = '#e27e8d'
    cyan    = '#70e1e8'
    white   = '#ffffff'
    """
)