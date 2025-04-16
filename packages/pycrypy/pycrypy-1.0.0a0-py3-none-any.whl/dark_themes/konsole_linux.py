# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

konsole_linux: Dict[str, Any] = loads(s = """\
    # Color theme ported from Konsole Linux colors

    [colors.primary]
    foreground = '#e3e3e3'
    bright_foreground = '#ffffff'
    background = '#1f1f1f'

    [colors.cursor]
    text = '#191622'
    cursor = '#f8f8f2'

    [colors.search]
    matches = { foreground = '#b2b2b2', background = '#b26818' }
    focused_match = { foreground = "CellBackground", background = "CellForeground" }

    [colors.normal]
    black   = '#000000'
    red     = '#b21818'
    green   = '#18b218'
    yellow  = '#b26818'
    blue    = '#1818b2'
    magenta = '#b218b2'
    cyan    = '#18b2b2'
    white   = '#b2b2b2'

    [colors.bright]
    black   = '#686868'
    red     = '#ff5454'
    green   = '#54ff54'
    yellow  = '#ffff54'
    blue    = '#5454ff'
    magenta = '#ff54ff'
    cyan    = '#54ffff'
    white   = '#ffffff'

    [colors.dim]
    black   = '#000000'
    red     = '#b21818'
    green   = '#18b218'
    yellow  = '#b26818'
    blue    = '#1818b2'
    magenta = '#b218b2'
    cyan    = '#18b2b2'
    white   = '#b2b2b2'
    """
)