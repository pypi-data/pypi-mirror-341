# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

Cobalt2: Dict[str, Any] = loads(s = """\
    # From the famous Cobalt2 sublime theme
    # Source  https//github.com/wesbos/cobalt2/tree/master/Cobalt2

    # Default colors
    [colors.primary]
    background = '#122637'
    foreground = '#ffffff'

    [colors.cursor]
    text = '#122637'
    cursor = '#f0cb09'

    # Normal colors
    [colors.normal]
    black   = '#000000'
    red     = '#ff0000'
    green   = '#37dd21'
    yellow  = '#fee409'
    blue    = '#1460d2'
    magenta = '#ff005d'
    cyan    = '#00bbbb'
    white   = '#bbbbbb'

    # Bright colors
    [colors.bright]
    black   = '#545454'
    red     = '#f40d17'
    green   = '#3bcf1d'
    yellow  = '#ecc809'
    blue    = '#5555ff'
    magenta = '#ff55ff'
    cyan    = '#6ae3f9'
    white   = '#ffffff'
    """
)