#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from importlib import import_module
from sys import stderr
from types import ModuleType
from typing import Any, Dict, List

# Definimos los nombres de los temas
light_themes: List[str] = [
    "alabaster",
    "ashes_light",
    "atom_one_light",
    "ayu_light",
    "catppuccin_latte",
    "enfocado_light",
    "everforest_light",
    "github_light_colorblind",
    "github_light_default",
    "github_light_high_contrast",
    "github_light",
    "github_light_tritanopia",
    "gruvbox_light",
    "gruvbox_material_hard_light",
    "gruvbox_material_medium_light",
    "high_contrast",
    "msx",
    "night_owlish_light",
    "noctis_lux",
    "nord_light",
    "papercolor_light",
    "papertheme",
    "pencil_light",
    "rose_pine_dawn",
    "solarized_light",
]

dark_themes: List[str] = [
    "afterglow",
    "alacritty_0_12",
    "ashes_dark",
    "base16_default_dark",
    "bluish",
    "breeze",
    "catppuccin_frappe",
    "catppuccin_macchiato",
    "catppuccin_mocha",
    "chicago95",
    "citylights",
    "Cobalt2",
    "dark_pastels",
    "deep_space",
    "doom_one",
    "dracula_plus",
    "enfocado_dark",
    "everforest_dark",
    "falcon",
    "flat_remix",
    "flexoki",
    "github_dark_dimmed",
    "github_dark",
    "gnome_terminal",
    "google",
    "gruvbox_dark",
    "gruvbox_material_hard_dark",
    "gruvbox_material_medium_dark",
    "gruvbox_material",
    "hardhacker",
    "hatsunemiku",
    "horizon_dark",
    "inferno",
    "iris",
    "kanagawa_dragon",
    "kanagawa_wave",
    "konsole_linux",
    "low_contrast",
    "Mariana",
    "marine_dark",
    "material_theme",
    "meliora",
    "monokai_pro",
    "monokai",
    "moonlight_ii_vscode",
    "nightfox",
    "nord",
    "one_dark",
    "papercolor_dark",
    "pencil_dark",
    "rainbow",
    "remedy_dark",
    "rose_pine_moon",
    "seashells",
    "smoooooth",
    "snazzy",
    "solarized_dark",
    "solarized_osaka",
    "taerminal",
    "tango_dark",
    "tender",
    "terminal_app",
    "tomorrow_night_bright",
    "tomorrow_night",
    "ubuntu",
    "vesper",
    "wombat",
    "zenburn",
]

recommended_themes: List[str] = [
    "alabaster_dark",
    "argonaut",
    "aura",
    "ayu_dark",
    "ayu_mirage",
    "baitong",
    "blood_moon",
    "bluescreen",
    "campbell",
    "carbonfox",
    "catppuccin",
    "challenger_deep",
    "cyber_punk_neon",
    "dark_pride",
    "dracula_inspired",
    "dracula",
    "github_dark_colorblind",
    "github_dark_default",
    "github_dark_high_contrast",
    "github_dark_tritanopia",
    "gotham",
    "greenscreen",
    "hyper",
    "iterm",
    "material_darker",
    "material_ocean",
    "material_theme_mod",
    "midnight_haze",
    "monokai_charcoal",
    "monokai_inspired",
    "nightfly",
    "night_owl",
    "nordic",
    "nord_inspired",
    "nord_wave",
    "oceanic_next",
    "omni",
    "onedark_inspired",
    "palenight",
    "pastel_dark",
    "rosepine_inspired",
    "rose_pine",
    "thelovelace",
    "tokyo_night",
    "tokyo_night_storm",
    "xterm",
]


async def load_themes(*, base_module: str, theme_name: str) -> Dict[str, Any]:
    """
    Dynamically imports a submodule and adds it to a themes dictionary.

    This function attempts to import a submodule specified by `theme_name` within
    the base module `base_module`, and stores it in a dictionary with the corresponding key.
    If the submodule is not found, an error message is printed to the standard error output.

    Args:
        base_module (str): Name of the base module containing the themes.
        theme_name (str): Name of the submodule (theme) to be imported.

    Returns:
        Dict[str, Any]: Dictionary containing the imported submodule under the key `theme_name`,
        or an empty dictionary if the import fails.
    """
    themes_dictionary: Dict[str, Any] = dict()
    try:
        theme: ModuleType = import_module(name=base_module + "." + theme_name)
        themes_dictionary[theme_name] = theme
    except ModuleNotFoundError:
        print(
            f"The module {theme_name} could not be found in {base_module}.",
            end="\n",
            flush=True,
            file=stderr,
        )
    return themes_dictionary


# async def cargar_temas(*, moduloBase: str, nombresTemas: List[str]) -> Dict[str, Any]:
#     """
#     Carga dinámicamente módulos de temas especificados y los almacena en un diccionario.

#     Parámetros:
#     - moduloBase (str): El nombre base del módulo desde donde se cargarán los submódulos de temas.
#     - nombresTemas (List[str]): Una lista de nombres de los temas (submódulos) a cargar.

#     Retorno:
#     - Dict[str, Any]: Un diccionario donde las claves son los nombres de los temas y los valores son los módulos importados.

#     Comportamiento:
#     - Itera sobre la lista de nombres de temas.
#     - Intenta importar cada tema como un submódulo del módulo base.
#     - Si la importación es exitosa, agrega el módulo al diccionario `temasDiccionario` con el nombre del tema como clave.
#     - Si un módulo no se puede encontrar, imprime un mensaje de error en stderr.
#     - Retorna el diccionario con los módulos importados.

#     Ejemplo de uso:
#     - Si se llama a `cargar_temas(moduloBase="temas", nombresTemas=["tema1", "tema2"])`, la función intentará importar `temas.tema1` y `temas.tema2`.
#     """
#     temasDiccionario: Dict[str, Any] = dict()
#     for nombre in nombresTemas:
#         try:
#             tema: ModuleType = import_module(name = f"{moduloBase}.{nombre}")
#             temasDiccionario[nombre] = tema
#         except ModuleNotFoundError: print(f"El módulo {nombre} no se pudo encontrar en {moduloBase}.", end="\n", file = stderr)
#     return temasDiccionario


"""
Para ver el contenido del módulo importado dinámicamente a través del diccionario recommended_themesDiccionario, puedes acceder a sus atributos y métodos utilizando la función dir() y luego imprimir los atributos que desees.

print(recommended_themesDiccionario.keys())
print(dir(recommended_themesDiccionario["onedark_inspired"]))

print(recommended_themesDiccionario["onedark_inspired"].onedark_inspired)
"""

"""
from typing import Dict, Any
from light_themes.alabaster import alabaster
from light_themes.ashes_light import ashes_light
from light_themes.atom_one_light import atom_one_light
from light_themes.ayu_light import ayu_light
from light_themes.catppuccin_latte import catppuccin_latte
from light_themes.enfocado_light import enfocado_light
from light_themes.everforest_light import everforest_light
from light_themes.github_light_colorblind import github_light_colorblind
from light_themes.github_light_default import github_light_default
from light_themes.github_light_high_contrast import github_light_high_contrast
from light_themes.github_light import github_light
from light_themes.github_light_tritanopia import github_light_tritanopia
from light_themes.gruvbox_light import gruvbox_light
from light_themes.gruvbox_material_hard_light import gruvbox_material_hard_light
from light_themes.gruvbox_material_medium_light import gruvbox_material_medium_light
from light_themes.high_contrast import high_contrast
from light_themes.msx import msx
from light_themes.night_owlish_light import night_owlish_light
from light_themes.noctis_lux import noctis_lux
from light_themes.nord_light import nord_light
from light_themes.papercolor_light import papercolor_light
from light_themes.papertheme import papertheme
from light_themes.pencil_light import pencil_light
from light_themes.rose_pine_dawn import rose_pine_dawn
from light_themes.solarized_light import solarized_light

from dark_themes.afterglow import afterglow
from dark_themes.alacritty_0_12 import alacritty_0_12
from dark_themes.ashes_dark import ashes_dark
from dark_themes.base16_default_dark import base16_default_dark
from dark_themes.bluish import bluish
from dark_themes.breeze import breeze
from dark_themes.catppuccin_frappe import catppuccin_frappe
from dark_themes.catppuccin_macchiato import catppuccin_macchiato
from dark_themes.catppuccin_mocha import catppuccin_mocha
from dark_themes.chicago95 import chicago95
from dark_themes.citylights import citylights
from dark_themes.Cobalt2 import Cobalt2
from dark_themes.dark_pastels import dark_pastels
from dark_themes.deep_space import deep_space
from dark_themes.doom_one import doom_one
from dark_themes.dracula_plus import dracula_plus
from dark_themes.enfocado_dark import enfocado_dark
from dark_themes.everforest_dark import everforest_dark
from dark_themes.falcon import falcon
from dark_themes.flat_remix import flat_remix
from dark_themes.flexoki import flexoki
from dark_themes.github_dark_dimmed import github_dark_dimmed
from dark_themes.github_dark import github_dark
from dark_themes.gnome_terminal import gnome_terminal
from dark_themes.google import google
from dark_themes.gruvbox_dark import gruvbox_dark
from dark_themes.gruvbox_material_hard_dark import gruvbox_material_hard_dark
from dark_themes.gruvbox_material_medium_dark import gruvbox_material_medium_dark
from dark_themes.gruvbox_material import gruvbox_material
from dark_themes.hardhacker import hardhacker
from dark_themes.hatsunemiku import hatsunemiku
from dark_themes.horizon_dark import horizon_dark
from dark_themes.inferno import inferno
from dark_themes.iris import iris
from dark_themes.kanagawa_dragon import kanagawa_dragon
from dark_themes.kanagawa_wave import kanagawa_wave
from dark_themes.konsole_linux import konsole_linux
from dark_themes.low_contrast import low_contrast
from dark_themes.Mariana import Mariana
from dark_themes.marine_dark import marine_dark
from dark_themes.material_theme import material_theme
from dark_themes.meliora import meliora
from dark_themes.monokai_pro import monokai_pro
from dark_themes.monokai import monokai
from dark_themes.moonlight_ii_vscode import moonlight_ii_vscode
from dark_themes.nightfox import nightfox
from dark_themes.nord import nord
from dark_themes.one_dark import one_dark
from dark_themes.papercolor_dark import papercolor_dark
from dark_themes.pencil_dark import pencil_dark
from dark_themes.rainbow import rainbow
from dark_themes.remedy_dark import remedy_dark
from dark_themes.rose_pine_moon import rose_pine_moon
from dark_themes.seashells import seashells
from dark_themes.smoooooth import smoooooth
from dark_themes.snazzy import snazzy
from dark_themes.solarized_dark import solarized_dark
from dark_themes.solarized_osaka import solarized_osaka
from dark_themes.taerminal import taerminal
from dark_themes.tango_dark import tango_dark
from dark_themes.tender import tender
from dark_themes.terminal_app import terminal_app
from dark_themes.tomorrow_night_bright import tomorrow_night_bright
from dark_themes.tomorrow_night import tomorrow_night
from dark_themes.ubuntu import ubuntu
from dark_themes.vesper import vesper
from dark_themes.wombat import wombat
from dark_themes.zenburn import zenburn

from recommended_themes.alabaster_dark import alabaster_dark
from recommended_themes.argonaut import argonaut
from recommended_themes.aura import aura
from recommended_themes.ayu_dark import ayu_dark
from recommended_themes.ayu_mirage import ayu_mirage
from recommended_themes.baitong import baitong
from recommended_themes.blood_moon import blood_moon
from recommended_themes.bluescreen import bluescreen
from recommended_themes.campbell import campbell
from recommended_themes.carbonfox import carbonfox
from recommended_themes.catppuccin import catppuccin
from recommended_themes.challenger_deep import challenger_deep
from recommended_themes.cyber_punk_neon import cyber_punk_neon
from recommended_themes.dark_pride import dark_pride
from recommended_themes.dracula_inspired import dracula_inspired
from recommended_themes.dracula import dracula
from recommended_themes.github_dark_colorblind import github_dark_colorblind
from recommended_themes.github_dark_default import github_dark_default
from recommended_themes.github_dark_high_contrast import github_dark_high_contrast
from recommended_themes.github_dark_tritanopia import github_dark_tritanopia
from recommended_themes.gotham import gotham
from recommended_themes.greenscreen import greenscreen
from recommended_themes.hyper import hyper
from recommended_themes.iterm import iterm
from recommended_themes.material_darker import material_darker
from recommended_themes.material_ocean import material_ocean
from recommended_themes.material_theme_mod import material_theme_mod
from recommended_themes.midnight_haze import midnight_haze
from recommended_themes.monokai_charcoal import monokai_charcoal
from recommended_themes.monokai_inspired import monokai_inspired
from recommended_themes.nightfly import nightfly
from recommended_themes.night_owl import night_owl
from recommended_themes.nordic import nordic
from recommended_themes.nord_inspired import nord_inspired
from recommended_themes.nord_wave import nord_wave
from recommended_themes.oceanic_next import oceanic_next
from recommended_themes.omni import omni
from recommended_themes.onedark_inspired import onedark_inspired
from recommended_themes.palenight import palenight
from recommended_themes.pastel_dark import pastel_dark
from recommended_themes.rosepine_inspired import rosepine_inspired
from recommended_themes.rose_pine import rose_pine
from recommended_themes.thelovelace import thelovelace
from recommended_themes.tokyo_night import tokyo_night
from recommended_themes.tokyo_night_storm import tokyo_night_storm
from recommended_themes.xterm import xterm

light_themesDiccionario: Dict[str, Any] = {
    "alabaster": alabaster,
    "ashes_light": ashes_light,
    "atom_one_light": atom_one_light,
    "ayu_light": ayu_light,
    "catppuccin_latte": catppuccin_latte,
    "enfocado_light": enfocado_light,
    "everforest_light": everforest_light,
    "github_light_colorblind": github_light_colorblind,
    "github_light_default": github_light_default,
    "github_light_high_contrast": github_light_high_contrast,
    "github_light": github_light,
    "github_light_tritanopia": github_light_tritanopia,
    "gruvbox_light": gruvbox_light,
    "gruvbox_material_hard_light": gruvbox_material_hard_light,
    "gruvbox_material_medium_light": gruvbox_material_medium_light,
    "high_contrast": high_contrast,
    "msx": msx,
    "night_owlish_light": night_owlish_light,
    "noctis_lux": noctis_lux,
    "nord_light": nord_light,
    "papercolor_light": papercolor_light,
    "papertheme": papertheme,
    "pencil_light": pencil_light,
    "rose_pine_dawn": rose_pine_dawn,
    "solarized_light": solarized_light
}


dark_themesDiccionario: Dict[str, Any] = {
    "afterglow": afterglow,
    "alacritty_0_12": alacritty_0_12,
    "ashes_dark": ashes_dark,
    "base16_default_dark": base16_default_dark,
    "bluish": bluish,
    "breeze": breeze,
    "catppuccin_frappe": catppuccin_frappe,
    "catppuccin_macchiato": catppuccin_macchiato,
    "catppuccin_mocha": catppuccin_mocha,
    "chicago95": chicago95,
    "citylights": citylights,
    "Cobalt2": Cobalt2,
    "dark_pastels": dark_pastels,
    "deep_space": deep_space,
    "doom_one": doom_one,
    "dracula_plus": dracula_plus,
    "enfocado_dark": enfocado_dark,
    "everforest_dark": everforest_dark,
    "falcon": falcon,
    "flat_remix": flat_remix,
    "flexoki": flexoki,
    "github_dark_dimmed": github_dark_dimmed,
    "github_dark": github_dark,
    "gnome_terminal": gnome_terminal,
    "google": google,
    "gruvbox_dark": gruvbox_dark,
    "gruvbox_material_hard_dark": gruvbox_material_hard_dark,
    "gruvbox_material_medium_dark": gruvbox_material_medium_dark,
    "gruvbox_material": gruvbox_material,
    "hardhacker": hardhacker,
    "hatsunemiku": hatsunemiku,
    "horizon_dark": horizon_dark,
    "inferno": inferno,
    "iris": iris,
    "kanagawa_dragon": kanagawa_dragon,
    "kanagawa_wave": kanagawa_wave,
    "konsole_linux": konsole_linux,
    "low_contrast": low_contrast,
    "Mariana": Mariana,
    "marine_dark": marine_dark,
    "material_theme": material_theme,
    "meliora": meliora,
    "monokai_pro": monokai_pro,
    "monokai": monokai,
    "moonlight_ii_vscode": moonlight_ii_vscode,
    "nightfox": nightfox,
    "nord": nord,
    "one_dark": one_dark,
    "papercolor_dark": papercolor_dark,
    "pencil_dark": pencil_dark,
    "rainbow": rainbow,
    "remedy_dark": remedy_dark,
    "rose_pine_moon": rose_pine_moon,
    "seashells": seashells,
    "smoooooth": smoooooth,
    "snazzy": snazzy,
    "solarized_dark": solarized_dark,
    "solarized_osaka": solarized_osaka,
    "taerminal": taerminal,
    "tango_dark": tango_dark,
    "tender": tender,
    "terminal_app": terminal_app,
    "tomorrow_night_bright": tomorrow_night_bright,
    "tomorrow_night": tomorrow_night,
    "ubuntu": ubuntu,
    "vesper": vesper,
    "wombat": wombat,
    "zenburn": zenburn
}

recommended_themesDiccionario: Dict[str, Any] = {
    "alabaster_dark": alabaster_dark,
    "argonaut": argonaut,
    "aura": aura,
    "ayu_dark": ayu_dark,
    "ayu_mirage": ayu_mirage,
    "baitong": baitong,
    "blood_moon": blood_moon,
    "bluescreen": bluescreen,
    "campbell": campbell,
    "carbonfox": carbonfox,
    "catppuccin": catppuccin,
    "challenger_deep": challenger_deep,
    "cyber_punk_neon": cyber_punk_neon,
    "dark_pride": dark_pride,
    "dracula_inspired": dracula_inspired,
    "dracula": dracula,
    "github_dark_colorblind": github_dark_colorblind,
    "github_dark_default": github_dark_default,
    "github_dark_high_contrast": github_dark_high_contrast,
    "github_dark_tritanopia": github_dark_tritanopia,
    "gotham": gotham,
    "greenscreen": greenscreen,
    "hyper": hyper,
    "iterm": iterm,
    "material_darker": material_darker,
    "material_ocean": material_ocean,
    "material_theme_mod": material_theme_mod,
    "midnight_haze": midnight_haze,
    "monokai_charcoal": monokai_charcoal,
    "monokai_inspired": monokai_inspired,
    "nightfly": nightfly,
    "night_owl": night_owl,
    "nordic": nordic,
    "nord_inspired": nord_inspired,
    "nord_wave": nord_wave,
    "oceanic_next": oceanic_next,
    "omni": omni,
    "onedark_inspired": onedark_inspired,
    "palenight": palenight,
    "pastel_dark": pastel_dark,
    "rosepine_inspired": rosepine_inspired,
    "rose_pine": rose_pine,
    "thelovelace": thelovelace,
    "tokyo_night": tokyo_night,
    "tokyo_night_storm": tokyo_night_storm,
    "xterm": xterm
}
"""
