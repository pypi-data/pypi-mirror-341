# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

gruvbox_dark: Dict[str, Any] = loads(s = """\
    # Colors (Gruvbox dark)

    # Default colors
    [colors.primary]
    # hard contrast background = = '#1d2021'
    background = '#282828'
    # soft contrast background = = '#32302f'
    foreground = '#ebdbb2'

    # Normal colors
    [colors.normal]
    black   = '#282828'
    red     = '#cc241d'
    green   = '#98971a'
    yellow  = '#d79921'
    blue    = '#458588'
    magenta = '#b16286'
    cyan    = '#689d6a'
    white   = '#a89984'

    # Bright colors
    [colors.bright]
    black   = '#928374'
    red     = '#fb4934'
    green   = '#b8bb26'
    yellow  = '#fabd2f'
    blue    = '#83a598'
    magenta = '#d3869b'
    cyan    = '#8ec07c'
    white   = '#ebdbb2'
    """
)