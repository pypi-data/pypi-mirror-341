# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

terminal_app: Dict[str, Any] = loads(s = """\
    # Colors (Terminal.app)

    # Default colors
    [colors.primary]
    background = '#000000'
    foreground = '#b6b6b6'

    # Normal colors
    [colors.normal]
    black   = '#000000'
    red     = '#990000'
    green   = '#00a600'
    yellow  = '#999900'
    blue    = '#0000b2'
    magenta = '#b200b2'
    cyan    = '#00a6b2'
    white   = '#bfbfbf'

    # Bright colors
    [colors.bright]
    black   = '#666666'
    red     = '#e50000'
    green   = '#00d900'
    yellow  = '#e5e500'
    blue    = '#0000ff'
    magenta = '#e500e5'
    cyan    = '#00e5e5'
    white   = '#e5e5e5'
    """
)