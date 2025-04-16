# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

zenburn: Dict[str, Any] = loads(s = """\
    # Colors (Zenburn)
    # Orginally designed by jnurmine for vim.

    # Default colors
    [colors.primary]
    background = '#3A3A3A'
    foreground = '#DCDCCC'

    # Normal colors
    [colors.normal]
    black   = '#1E2320'
    red     = '#D78787'
    green   = '#60B48A'
    yellow  = '#DFAF8F'
    blue    = '#506070'
    magenta = '#DC8CC3'
    cyan    = '#8CD0D3'
    white   = '#DCDCCC'

    # Bright colors
    [colors.bright]
    black   = '#709080'
    red     = '#DCA3A3'
    green   = '#C3BF9F'
    yellow  = '#F0DFAF'
    blue    = '#94BFF3'
    magenta = '#EC93D3'
    cyan    = '#93E0E3'
    white   = '#FFFFFF'
    """
)