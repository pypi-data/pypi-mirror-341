# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads

catppuccin: Dict[str, Any] = loads(s = """\
    # Catppuccino theme scheme for Alacritty

    [colors.primary]
    background = '#1E1E2E'
    foreground = '#D6D6D6'

    [colors.cursor]
    text = '#1E1E2E'
    cursor = '#D9D9D9'

    [colors.normal]
    black = '#181A1F'
    red = '#E86671'
    green = '#98C379'
    yellow = '#E5C07B'
    blue = '#61AFEF'
    magenta = '#C678DD'
    cyan = '#54AFBC'
    white = '#ABB2BF'

    [colors.bright]
    black = '#5C6370'
    red = '#E86671'
    green = '#98C379'
    yellow = '#E5C07B'
    blue = '#61AFEF'
    magenta = '#C678DD'
    cyan = '#54AFBC'
    white = '#F7F7F7'

    [colors.dim]
    black = '#5C6370'
    red = '#74423F'
    green = '#98C379'
    yellow = '#E5C07B'
    blue = '#61AFEF'
    magenta = '#6E4962'
    cyan = '#5C8482'
    white = '#828282'
    """
)