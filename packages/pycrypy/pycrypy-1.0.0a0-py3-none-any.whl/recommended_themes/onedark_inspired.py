# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from typing import Dict, Any
from toml import loads
                         
onedark_inspired: Dict[str, Any] = loads(s = """\
    # Themes Colors (onedark-inspired)

    # Default colors onedark-inspired
    [colors.primary]
    background = '#1e2127'
    foreground = '#abb2bf'

    # Bright and dim foreground colors
    #
    # The dimmed foreground color is calculated automatically if it is not present.
    # If the bright foreground color is not set, or `draw_bold_text_with_bright_colors`
    # is `false`, the normal foreground color will be used.
    #dim_foreground: '#9a9a9a'
    bright_foreground = '#e6efff'

    # Cursor colors
    #
    # Colors which should be used to draw the terminal cursor. If these are unset,
    # the cursor color will be the inverse of the cell color.
    #cursor:
    #  text: '#000000'
    #  cursor: '#ffffff'

    # Normal colors onedark-inspired
    [colors.normal]
    black = '#1e2127'
    red = '#ffffff'
    green = '#98c379'
    yellow = '#d19a66'
    blue = '#61afef'
    magenta = '#c678dd'
    cyan = '#56b6c2'
    white = '#e6efff'
    """
)