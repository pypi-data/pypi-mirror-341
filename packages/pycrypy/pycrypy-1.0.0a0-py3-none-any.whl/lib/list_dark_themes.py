#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from sys import stdout
from typing import List, Tuple

from prettytable import PrettyTable

from lib.format_ansi_color import bold, italic

dark_themes: List[Tuple[str, ...]] = [
    (
        "afterglow",
        "Dark theme with warm tones that mimic the glow of sunset.",
    ),
    (
        "alacritty_0_12",
        "Specific theme for version 0.12 of Alacritty, with dark and contrasting colors.",
    ),
    ("ashes_dark", "Dark theme with a palette of grays and muted tones."),
    (
        "base16_default_dark",
        "Dark theme based on the Base16 palette with a clean design.",
    ),
    ("bluish", "Dark theme with deep and contrasting blue tones."),
    ("breeze", "Dark theme based on the Breeze style with soft colors."),
    (
        "catppuccin_frappe",
        "Variant of the Catppuccin theme with a frappé style, soft and dark.",
    ),
    (
        "catppuccin_macchiato",
        "Variant of the Catppuccin theme with a macchiato style, soft and dark.",
    ),
    (
        "catppuccin_mocha",
        "Variant of the Catppuccin theme with a mocha style, soft and dark.",
    ),
    ("chicago95", "Theme inspired by the colors of the Chicago 95 operating system."),
    (
        "citylights",
        "Dark theme with colors inspired by city lights at night.",
    ),
    ("Cobalt2", "Dark theme with a deep blue and contrasting color scheme."),
    ("dark_pastels", "Dark theme with muted pastel colors."),
    ("deep_space", "Dark theme inspired by the colors of deep space."),
    ("doom_one", "Dark theme with a style inspired by Doom, with intense colors."),
    (
        "dracula_plus",
        "Variant of the Dracula theme with additional adjustments for a darker style.",
    ),
    ("enfocado_dark", "Dark theme focused on readability and contrast."),
    ("everforest_dark", "Dark theme with a green and dark wood palette."),
    ("falcon", "Dark theme with metallic tones and an aggressive style."),
    ("flat_remix", "Dark theme with a flat and modern design."),
    ("flexoki", "Dark theme with a flexible and contrasting palette."),
    ("github_dark_dimmed", "GitHub dark theme with slightly dimmed colors."),
    ("github_dark", "GitHub dark theme with contrasting and modern colors."),
    ("gnome_terminal", "Dark theme inspired by the GNOME terminal."),
    ("google", "Dark theme inspired by Google's dark design colors."),
    (
        "gruvbox_dark",
        "Dark theme based on the Gruvbox color scheme with high contrast.",
    ),
    (
        "gruvbox_material_hard_dark",
        "Variant of the Gruvbox theme with a darker and more contrasting style.",
    ),
    (
        "gruvbox_material_medium_dark",
        "Variant of the Gruvbox theme with a dark but less intense style.",
    ),
    ("gruvbox_material", "Gruvbox Material theme with dark and comfortable colors."),
    ("hardhacker", "Dark theme with an aggressive and modern design."),
    (
        "hatsunemiku",
        "Dark theme inspired by the Hatsune Miku character with vibrant colors.",
    ),
    (
        "horizon_dark",
        "Dark theme with a color palette inspired by the night horizon.",
    ),
    ("inferno", "Dark theme with warm tones inspired by fire and lava."),
    ("iris", "Dark theme with purple and soft colors."),
    (
        "kanagawa_dragon",
        "Dark theme inspired by Japanese mythology with dark and vibrant tones.",
    ),
    (
        "kanagawa_wave",
        "Dark theme inspired by Japanese waves with intense colors.",
    ),
    ("konsole_linux", "Dark theme based on the Konsole terminal from Linux."),
    ("low_contrast", "Dark theme with low contrast for a smoother experience."),
    (
        "Mariana",
        "Dark theme with a palette inspired by the depth of the Mariana Trench.",
    ),
    ("marine_dark", "Dark theme with deep marine colors."),
    ("material_theme", "Dark theme based on the Material Design style."),
    ("meliora", "Dark theme with warm and dark colors."),
    ("monokai_pro", "Variant of the classic Monokai theme with a modern style."),
    ("monokai", "Classic dark theme with vibrant colors and high contrast."),
    (
        "moonlight_ii_vscode",
        "Dark theme with a color palette inspired by moonlight.",
    ),
    ("nightfox", "Dark theme with a palette inspired by the night and foxes."),
    ("nord", "Dark theme based on the Nordic style with cool and soft colors."),
    ("one_dark", "Dark theme inspired by the One Dark theme."),
    ("papercolor_dark", "Dark theme with paper colors and a soft design."),
    ("pencil_dark", "Dark theme with a color scheme inspired by pencils."),
    ("rainbow", "Dark theme with a color palette inspired by the rainbow."),
    ("remedy_dark", "Dark theme with colors that help reduce eye strain."),
    (
        "rose_pine_moon",
        "Dark theme with soft and moon-inspired tones from Rose Pine.",
    ),
    ("seashells", "Dark theme with a palette inspired by seashells."),
    ("smoooooth", "Dark theme with a palette of soft and relaxing colors."),
    ("snazzy", "Dark theme with vibrant colors and a striking style."),
    ("solarized_dark", "Dark theme based on the Solarized color scheme."),
    (
        "solarized_osaka",
        "Variant of the Solarized theme with a palette inspired by Osaka.",
    ),
    ("taerminal", "Dark theme with a modern and contrasting style."),
    ("tango_dark", "Dark theme based on the Tango style with intense colors."),
    ("tender", "Dark theme with a palette of soft and pleasant colors."),
    ("terminal_app", "Dark theme with a design focused on usability."),
    (
        "tomorrow_night_bright",
        "Dark theme with bright colors inspired by the night.",
    ),
    ("tomorrow_night", "Dark theme with colors inspired by the night and dawn."),
    ("ubuntu", "Dark theme inspired by Ubuntu's design."),
    ("vesper", "Dark theme with a palette inspired by the calm of the evening."),
    ("wombat", "Dark theme with intense colors and an aggressive style."),
    ("zenburn", "Dark theme with muted colors and a relaxing style."),
]


# List dark themes: Abbreviated: list_dark_themes
async def list_dark_themes() -> None:
    """
    ### This function lists the recommended dark themes for Alacritty
    - Example:

    ```python
    list_dark_themes()
    ```
    """
    # Crear la tabla
    table: PrettyTable = PrettyTable()
    table.field_names = [
        bold(text="Nombre del Tema", color="green"),
        bold(text="Descripción", color="green"),
    ]

    # Añadir filas a la tabla
    theme: str
    descripcion: str
    for theme, descripcion in dark_themes:
        table.add_row(
            row=[
                italic(text=theme, color="cyan"),
                italic(text=descripcion, color="blue"),
            ],
            divider=False,
        )

    # Imprimir la tabla
    print(table, end="\n", flush=True, file=stdout)

    return None
