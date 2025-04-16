#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from sys import stdout
from typing import List, Tuple

from prettytable import PrettyTable

from lib.format_ansi_color import bold, italic

recommended_themes: List[Tuple[str, ...]] = [
    ("alabaster_dark", "Dark theme with an elegant and minimalist style."),
    ("argonaut", "Theme with vibrant colors and a dark background."),
    ("aura", "Theme with a soft and modern color palette."),
    ("ayu_dark", "Dark theme with bluish and greenish accents."),
    ("ayu_mirage", "Variation of the Ayu theme with a unique style."),
    ("baitong", "Dark theme with high contrast."),
    ("blood_moon", "Theme with red and dark tones."),
    ("bluescreen", "Inspired by blue error screens."),
    ("campbell", "Theme based on the colors of the Campbell logo."),
    ("carbonfox", "Dark theme with charcoal tones."),
    ("catppuccin", "Soft and cozy theme with a pastel style."),
    ("challenger_deep", "Theme with a deep and dark color scheme."),
    ("cyber_punk_neon", "Theme with neon colors and a cyberpunk style."),
    ("dark_pride", "Dark theme with pride-toned accents."),
    ("dracula_inspired", "Inspired by the popular Dracula theme."),
    ("dracula", "Dark theme with a rich and contrasting palette."),
    ("github_dark_colorblind", "Version of the GitHub theme for colorblind users."),
    ("github_dark_default", "Default dark theme from GitHub."),
    ("github_dark_high_contrast", "High contrast version of the GitHub dark theme."),
    ("github_dark_tritanopia", "Adaptation for tritanopia of the GitHub theme."),
    ("gotham", "Theme with an urban and modern style."),
    ("greenscreen", "Theme with a vibrant green background."),
    ("hyper", "Theme inspired by the Hyper terminal."),
    ("iterm", "Theme based on the colors of the iTerm terminal."),
    ("material_darker", "Dark variant of the Material theme."),
    ("material_ocean", "Theme inspired by the Material Ocean aesthetic."),
    ("material_theme_mod", "Modification of the Material Theme."),
    ("midnight_haze", "Theme with a dark and hazy background."),
    ("monokai_charcoal", "Variant of the Monokai theme with charcoal tones."),
    ("monokai_inspired", "Inspired by the classic Monokai theme."),
    ("nightfly", "Theme with a nocturnal and deep style."),
    ("night_owl", "Dark theme with accents in blue tones."),
    ("nordic", "Theme inspired by northern colors."),
    ("nord_inspired", "Inspired by the Nordic theme with adjustments."),
    ("nord_wave", "Variant of the Nordic theme with a wave touch."),
    ("oceanic_next", "Theme with an oceanic color scheme."),
    ("omni", "Theme with a dynamic color palette."),
    ("onedark_inspired", "Inspired by the One Dark theme."),
    ("palenight", "Theme with a nocturnal and relaxed style."),
    ("pastel_dark", "Dark theme with pastel colors."),
    ("rosepine_inspired", "Inspired by the Rose Pine theme."),
    ("rose_pine", "Theme with a palette of pink and pine colors."),
    ("thelovelace", "Theme with a romantic and warm style."),
    ("tokyo_night", "Theme inspired by Tokyo's night."),
    ("tokyo_night_storm", "Variant of the Tokyo Night theme with a stormy touch."),
    ("xterm", "Theme inspired by the classic xterm style."),
]


# List recommended themes: Abbreviated: ltr
async def list_recommended_themes() -> None:
    """
    ### This function lists the recommended themes for Alacritty
    - Example:

    ```python
    list_recommended_themes()
    ```
    """
    # Create the table
    table: PrettyTable = PrettyTable()
    table.field_names = [
        bold(text="Theme Name", color="green"),
        bold(text="Description", color="green"),
    ]

    # Add rows to the table
    theme: str
    description: str
    for theme, description in recommended_themes:
        table.add_row(
            row=[
                italic(text=theme, color="cyan"),
                italic(text=description, color="blue"),
            ],
            divider=False,
        )

    # Print the table
    print(table, end="\n", flush=True, file=stdout)

    return None
