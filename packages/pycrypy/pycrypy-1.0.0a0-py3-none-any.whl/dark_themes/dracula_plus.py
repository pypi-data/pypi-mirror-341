# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

dracula_plus: Dict[str, Any] = loads(s = """\
    # Colors (Dracula+)

    [colors.primary]
    background = '#212121'
    foreground = '#F8F8F2'

    [colors.cursor]
    text = '#0E1415'
    cursor = '#ECEFF4'

    [colors.normal]
    black = '#21222C'
    red = '#FF5555'
    green = '#50FA7B'
    yellow = '#FFCB6B'
    blue = '#82AAFF'
    magenta = '#C792EA'
    cyan = '#8BE9FD'
    white = '#F8F9F2'

    [colors.bright]
    black = '#545454'
    red = '#FF6E6E'
    green = '#69FF94'
    yellow = '#FFCB6B'
    blue = '#D6ACFF'
    magenta = '#FF92DF'
    cyan = '#A4FFFF'
    white = '#F8F8F2'
    """
)