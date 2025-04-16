# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

monokai_charcoal: Dict[str, Any] = loads(s = """\
    # Colours (Monokai Charcoal)

    # Default Colours
    [colors.primary]
    background = '#000000'
    foreground = '#FFFFFF'

    # Normal Colours
    [colors.normal]
    black   = '#1a1a1a'
    red     = '#f4005f'
    green   = '#98e024'
    yellow  = '#fa8419'
    blue    = '#9d65ff'
    magenta = '#f4005f'
    cyan    = '#58d1eb'
    white   = '#c4c5b5'

    # Bright Colours
    [colors.bright]
    black   = '#625e4c'
    red     = '#f4005f'
    green   = '#98e024'
    yellow  = '#e0d561'
    blue    = '#9d65ff'
    magenta = '#f4005f'
    cyan    = '#58d1eb'
    white   = '#f6f6ef'
    """
)