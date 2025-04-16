# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

papercolor_dark: Dict[str, Any] = loads(s = """\
    # Colors (PaperColor - Dark)

    # Default colors
    [colors.primary]
    background = '#1c1c1c'
    foreground = '#808080'

    [colors.cursor]
    text = '#1c1c1c'
    cursor = '#808080'

    # Normal colors
    [colors.normal]
    black   = '#1c1c1c'
    red     = '#af005f'
    green   = '#5faf00'
    yellow  = '#d7af5f'
    blue    = '#5fafd7'
    magenta = '#808080'
    cyan    = '#d7875f'
    white   = '#d0d0d0'

    # Bright colors
    [colors.bright]
    black   = '#585858'
    red     = '#5faf5f'
    green   = '#afd700'
    yellow  = '#af87d7'
    blue    = '#ffaf00'
    magenta = '#ffaf00'
    cyan    = '#00afaf'
    white   = '#5f8787'
    """
)