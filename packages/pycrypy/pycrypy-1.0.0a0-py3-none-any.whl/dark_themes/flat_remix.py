# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

flat_remix: Dict[str, Any] = loads(s = """\
    [colors.primary]
    background = '#272a34'
    foreground = '#FFFFFF'

    [colors.normal]
    black   = '#1F2229'
    red     = '#EC0101'
    green   = '#47D4B9'
    yellow  = '#FF8A18'
    blue    = '#277FFF'
    magenta = '#D71655'
    cyan    = '#05A1F7'
    white   = '#FFFFFF'

    [colors.bright]
    black   = '#1F2229'
    red     = '#D41919'
    green   = '#5EBDAB'
    yellow  = '#FEA44C'
    blue    = '#367bf0'
    magenta = '#BF2E5D'
    cyan    = '#49AEE6'
    white   = '#FFFFFF'
    """
)