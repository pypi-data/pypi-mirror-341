#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from sys import stdout
from typing import List, Tuple

from prettytable import PrettyTable

from lib.format_ansi_color import bold, italic

# List of recommended light themes with descriptions
light_themes: List[Tuple[str, ...]] = [
    ("alabaster", "A light theme with a clean and minimalist background."),
    ("ashes_light", "A light theme with soft tones and low contrasts."),
    ("atom_one_light", "A light theme with bright and accented colors."),
    ("ayu_light", "A light theme with a soft tone and gentle colors."),
    ("catppuccin_latte", "A light theme with colors inspired by latte coffee."),
    (
        "enfocado_light",
        "A light theme focused on readability and contrast.",
    ),
    (
        "everforest_light",
        "A light theme with soft green tones and a natural feel.",
    ),
    (
        "github_light_colorblind",
        "A light theme designed to be accessible for colorblind users.",
    ),
    ("github_light_default", "The default light theme of GitHub."),
    ("github_light_high_contrast", "A GitHub light theme with high contrast."),
    ("github_light", "A light theme based on GitHub's style."),
    (
        "github_light_tritanopia",
        "A GitHub light theme designed for users with color vision deficiency.",
    ),
    ("gruvbox_light", "A light theme with a retro style and soft colors."),
    (
        "gruvbox_material_hard_light",
        "A light theme with a material style and hard colors.",
    ),
    (
        "gruvbox_material_medium_light",
        "A light theme with a material style and medium colors.",
    ),
    (
        "high_contrast",
        "A light theme with high contrast to improve readability.",
    ),
    ("msx", "A light theme with colors inspired by MSX systems aesthetics."),
    ("night_owlish_light", "A light theme with tones inspired by the night."),
    ("noctis_lux", "A light theme with an elegant design and soft colors."),
    (
        "nord_light",
        "A light theme inspired by the Nord color scheme with soft tones.",
    ),
    (
        "papercolor_light",
        "A light theme with a paper-colored background and soft tones.",
    ),
    (
        "papertheme",
        "A light theme with a paper-colored background and a minimalist palette.",
    ),
    ("pencil_light", "A light theme with colors inspired by pencils and soft tones."),
    ("rose_pine_dawn", "A light theme with soft tones inspired by dawn."),
    (
        "solarized_light",
        "A light theme based on the Solarized color scheme with soft tones.",
    ),
]


# Listar temas light: Abreviado: ltl
async def list_light_themes() -> None:
    """
    ### This function lists the recommended light themes for Alacritty
    - Example:

    ```python
    list_light_themes()
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
    for theme, description in light_themes:
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
