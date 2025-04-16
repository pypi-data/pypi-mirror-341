# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

nordic: Dict[str, Any] = loads(s = """\
    # Colors (Nordic)

    [colors.primary]
    background = '#242933'
    foreground = '#BBBDAF'

    [colors.normal]
    black = '#191C1D'
    red = '#BD6062'
    green = '#A3D6A9'
    yellow = '#F0DFAF'
    blue = '#8FB4D8'
    magenta = '#C7A9D9'
    cyan = '#B6D7A8'
    white = '#BDC5BD'

    [colors.bright]
    black = '#727C7C'
    red = '#D18FAF'
    green = '#B7CEB0'
    yellow = '#BCBCBC'
    blue = '#E0CF9F'
    magenta = '#C7A9D9'
    cyan = '#BBDA97'
    white = '#BDC5BD'

    [colors.selection]
    text = '#000000'
    background = '#F0DFAF'
    """
)