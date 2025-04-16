# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me


import os
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv, stderr, stdout

sys.path.append(os.path.abspath(path=os.path.join(os.path.dirname(p=__file__), "..")))

from typing import List, NoReturn, Optional, Type, Union

from config.path import (  # Verficar Si Directorio Existe -> Abreviado: vsde
    alacritty_toml_path,
    verify_if_directory_exists,
)
from lib.change_cursor_blinking import (
    change_cursor_blinking,  # Cambiar cursor blinking -> Abreviado: ccb
)
from lib.change_cursor_shape import (
    change_cursor_shape,  # Cambiar cursor shape -> Abreviado: ccs
)
from lib.change_cursor_thickness import (
    change_cursor_thickness,  # Cambiar cursor thickness -> Abreviado: cct
)
from lib.change_font import change_font  # Cambiar fuente -> Abreviado: cf
from lib.change_font_size import (
    change_font_size,  # Cambiar tamaño de fuente -> Abreviado: ctf
)
from lib.change_font_style import (
    change_font_style,  # Cambiar estilo de fuente -> Abreviado: cef
)
from lib.change_opacity import change_opacity  # Cambiar opacidad -> Abreviado: co
from lib.change_padding import change_padding  # Cambiar padding -> Abreviado: cp
from lib.change_theme_path import (
    change_theme_path,  # Cambiar theme ruta -> Abreviado: ctr
)
from lib.format_ansi_color import bold, italic
from lib.list_dark_themes import list_dark_themes
from lib.list_light_themes import list_light_themes
from lib.list_recommended_themes import list_recommended_themes
from lib.load_new_theme import load_new_theme  # Cargar nuevo theme -> Abreviado: cnt

"""
```python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### `sys.path.append(...)`

- **`sys.path`**: Es una lista en Python que contiene las rutas donde el intérprete de Python buscará los módulos a importar.
- **`sys.path.append(...)`**: Añade un nuevo directorio a la lista `sys.path`. Esto significa que Python buscará módulos también en el directorio que se añada aquí.

### `os.path.abspath(...)`

- **`os.path.abspath(path)`**: Convierte una ruta relativa en una ruta absoluta. Esto es útil para asegurarse de que siempre se trabaje con rutas completas, independientemente del directorio actual desde el que se ejecute el script.

### `os.path.join(...)`

- **`os.path.join(*paths)`**: Junta uno o más componentes de ruta de una manera independiente del sistheme operativo. En este caso, se están juntando dos componentes:
  - `os.path.dirname(__file__)`: El directorio donde se encuentra el fichero actual (`__file__`).
  - `'..'`: El directorio padre del directorio actual.

### `os.path.dirname(...)`

- **`os.path.dirname(path)`**: Devuelve la ruta del directorio de un fichero. Aquí, está recibiendo `__file__`, que es una variable que contiene la ruta del fichero Python que se está ejecutando.

### `__file__`

- **`__file__`**: Es una variable que contiene la ruta del fichero Python que se está ejecutando.

### Juntando todo:

1. **`os.path.dirname(__file__)`**: Obtiene la ruta del directorio donde se encuentra el fichero Python que se está ejecutando.
2. **`os.path.join(os.path.dirname(__file__), '..')`**: Junta la ruta del directorio del fichero actual con `'..'`, que representa el directorio padre, obteniendo así la ruta del directorio padre del fichero actual.
3. **`os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))`**: Convierte esta ruta relativa del directorio padre en una ruta absoluta.
4. **`sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`: Añade esta ruta absoluta del directorio padre a `sys.path`, lo que permite importar módulos desde el directorio padre del fichero actual.

En resumen, esta línea de código añade el directorio padre del fichero actual al `sys.path`, permitiendo importar módulos desde ese directorio.
"""

"""
StackOverflow forum on how to parse multiple arguments into a list:
https://stackoverflow.com/questions/15753701/how-can-i-pass-a-list-as-a-command-line-argument-with-argparse

Forum: No async lambda:
https://stackoverflow.com/questions/40746213/how-to-use-await-in-a-python-lambda
"""


class Cli:
    """
    The Cli class is part of the pycrypy program and provides a Command-Line Interface (CLI) to easily configure Alacritty, a highly customizable terminal emulator.

    Through various arguments and options, users can modify settings such as the theme, font, font size, font style, opacity, padding, and cursor shape, among others. The class also includes options to list recommended, dark, and light themes, display the program version, and enable a verbose output mode.

    This class simplifies the customization of Alacritty directly from the terminal, offering a quick and convenient configuration experience.
    """

    def __init__(self: "Cli") -> None:
        self.__version__: str = "1.0.0.alpha0"
        "* Version de la utilidad pycrypy"
        self.parser = ArgumentParser(
            prog=bold(text="pycrypy", color="white"),  # Program name displayed in help
            description=bold(
                text="pycrypy is a command-line tool designed to easily configure Alacritty options from the terminal using Python.",
                color="blue",
            ),  # Brief program description
            add_help=True,  # Automatically adds the -h/--help option to display help
            epilog=italic(
                text="Enjoy configuring your Alacritty with pycrypy!", color="green"
            ),  # Message at the end of the help
            exit_on_error=False,  # Controls whether the program should exit after printing an error message
        )

        self.parser.add_argument(
            "-t",
            "--theme",
            nargs="*",
            default=None,
            type=str,
            required=False,
            help=italic(text="Change the theme used by Alacritty", color="cyan"),
        )

        self.parser.add_argument(
            "-P",
            "--theme-path",
            dest="theme_path",
            type=str,
            default=False,
            nargs="?",
            required=False,
            help=italic(
                text="Absolute or relative path of the theme to apply in the Alacritty terminal",
                color="cyan",
            ),
        )

        self.parser.add_argument(
            "-f",
            "--font",
            nargs="*",
            default=None,
            type=str,
            required=False,
            help=italic(text="Change the font used by Alacritty", color="cyan"),
        )

        self.parser.add_argument(
            "-F",
            "--font-size",
            dest="fontSize",
            type=str,
            default=False,
            nargs="?",
            required=False,
            help=italic(text="Change the font size", color="cyan"),
        )

        self.parser.add_argument(
            "-s",
            "--style",
            nargs="*",
            default=None,
            type=str,
            required=False,
            help=italic(
                text="Change the font style: Normal | Bold | Italic | Underline",
                color="cyan",
            ),
        )

        self.parser.add_argument(
            "-o",
            "--opacity",
            nargs="*",
            type=str,
            default=None,
            required=False,
            help=italic(
                text="Change the opacity of the Alacritty terminal", color="cyan"
            ),
        )

        self.parser.add_argument(
            "-p",
            "--padding",
            nargs="*",
            metavar=("X", "Y"),
            default=None,
            type=str,
            required=False,
            help=italic(
                text="Change the padding of the Alacritty terminal", color="cyan"
            ),
        )

        self.parser.add_argument(
            "-S",
            "--cursor-shape",
            dest="cursorShape",
            type=str,
            default=False,
            nargs="?",
            required=False,
            help=italic(
                text="Defines the cursor shape: Block | Underline | Beam",
                color="cyan",
            ),
        )

        self.parser.add_argument(
            "-B",
            "--cursor-blinking",
            dest="cursor_blinking",
            type=str,
            default=False,
            nargs="?",
            required=False,
            help=italic(
                text="Defines if the cursor blinks: Never | Off | On | Always",
                color="cyan",
            ),
        )

        self.parser.add_argument(
            "-T",
            "--cursor-thickness",
            dest="cursor_thickness",
            type=str,
            default=False,
            nargs="?",
            required=False,
            help=italic(text="Defines the cursor thickness", color="cyan"),
        )

        self.parser.add_argument(
            "-R",
            "--theme-recommendations",
            dest="theme_recommendations",
            action="store_true",
            required=False,
            help=italic(text="List recommended themes for Alacritty", color="cyan"),
        )

        self.parser.add_argument(
            "-D",
            "--theme-dark",
            dest="theme_dark",
            action="store_true",
            required=False,
            help=italic(text="List dark themes for Alacritty", color="cyan"),
        )

        self.parser.add_argument(
            "-L",
            "--theme-light",
            dest="theme_light",
            action="store_true",
            required=False,
            help=italic(text="List light themes for Alacritty", color="cyan"),
        )

        self.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            required=False,
            help=italic(text="Enable verbose mode", color="cyan"),
        )

        self.parser.add_argument(
            "-V",
            "--version",
            action="store_true",
            required=False,
            help=italic(
                text="Show the program version and author information",
                color="cyan",
            ),
        )

        # checkeamos que al menos haya un argumento
        if len(argv) == 1:
            self.parser.print_help(file=stderr)
            exit(code=1)
        return None

    @property
    async def version(self: "Cli") -> str:
        return self.__version__

    @version.setter
    async def version(self: "Cli", version: str) -> None:
        self.__version__ = version
        return None

    @version.deleter
    async def version(self: "Cli") -> None:
        del self.__version__
        return None

    async def parse_args(self: "Cli") -> Namespace:
        """
        Parse the command-line arguments using the configured argument parser.

        This asynchronous method utilizes the `self.parser` instance to parse
        the arguments provided via the command line and returns them as a
        `Namespace` object.

        Returns:
            Namespace: An object containing the parsed command-line arguments.
        """
        # Este método debería devolver los argumentos parseados
        return self.parser.parse_args()

    async def version_pycrypy(self: "Cli") -> str:
        """
        This function returns the author's information and the version of pycrypy.
        """
        autor: str = bold(text="Autor: ", color="cyan") + italic(
            text="Daniel Benjamin Perez Morales\n", color="green"
        )
        github: str = bold(text="GitHub: ", color="cyan") + italic(
            text="https://github.com/D4nitrix13\n", color="green"
        )
        gitlab: str = bold(text="GitLab: ", color="cyan") + italic(
            text="https://gitlab.com/D4nitrix13\n", color="green"
        )
        email: str = bold(text="Email: ", color="cyan") + italic(
            text="danielperezdev@proton.me\n", color="green"
        )
        version: str = bold(text="pycrypy Version: ", color="cyan") + italic(
            text=f"`v{self.__version__}`\n", color="green"
        )
        return autor + github + gitlab + email + version

    async def validation_flags_theme(self: "Cli", flag: str) -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flags `-t` and `-P`.
        """
        print(
            bold(
                text="Error: You must provide a theme when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(
            italic(text=f"-{flag}.", color="green"), end="\n", flush=True, file=stderr
        )
        print(
            bold(
                text="To see the available themes, use one of the following flags:",
                color="cyan",
            ),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(bold(text="-R ", color="green"), end="", flush=True, file=stderr)
        print(
            italic(text="Displays the recommended themes.", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -R", color="white"),
            end="\n\n",
            flush=True,
            file=stderr,
        )

        print(bold(text="-D ", color="green"), end="", flush=True, file=stderr)
        print(
            italic(text="Displays the dark themes.", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -D", color="white"),
            end="\n\n",
            flush=True,
            file=stderr,
        )

        print(bold(text="-L ", color="green"), end="", flush=True, file=stderr)
        print(
            italic(text="Displays the light themes.", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -L", color="white"),
            end="\n\n",
            flush=True,
            file=stderr,
        )

        print(bold(text="-P ", color="green"), end="", flush=True, file=stderr)
        print(
            italic(
                text="Absolute or relative path of the theme to apply it in the Alacritty terminal.",
                color="white",
            ),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(
                text="pycrypy -P /home/user/.config/alacritty/themes/mytheme.toml",
                color="white",
            ),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def validation_flags_font(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-f`.
        """
        print(
            bold(
                text="Error: You must provide the font name when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-f.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -f Cascadia Code NF", color="white"),
            end="\n",
            file=stderr,
        )
        return None

    async def validation_flags_font_size(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-F`.
        """
        print(
            bold(
                text="Error: You must provide the number (float) for the font size when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-F.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -F 16.5", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def validation_flags_font_style(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-s`.
        """
        print(
            bold(
                text="Error: You must provide the style name to apply to the font when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-s.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -s Bold Italic", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def validation_flags_opacity(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-o`.
        """
        print(
            bold(
                text="Error: You must provide the number (float) for opacity when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-o.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -o 0.7", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def cast_string_to_numeric(
        self, variable: Union[str, bool], tipo: Type[Union[float, int]]
    ) -> Union[float, int, bool, str, NoReturn]:
        """
        Converts a string to a numeric type (int or float).

        Parameters:
        - variable (str): The string to convert.
        - tipo (Type[Union[float, int]]): The target data type (int or float).

        Returns:
        - Union[float, int, None]: The converted value if successful. Returns None if an error occurs.

        Behavior:
        - If 'tipo' is 'int', attempts to convert 'variable' to an integer.
        - If 'tipo' is 'float', attempts to convert 'variable' to a float.
        - If a ValueError occurs, prints an error message and returns None.
        """
        try:
            # Check if the type is int or float and the variable is not False
            if tipo is int and variable:
                return int(variable)
            elif tipo is float and variable:
                return float(variable)
            else:
                return variable
        except ValueError:
            print(
                bold(
                    text=f"Error: The provided value `{variable}` must be of type ",
                    color="red",
                ),
                end="",
                file=stderr,
            )
            print(
                italic(text="int" if tipo is int else "float", color="green"),
                end="\n",
                file=stderr,
            )
        exit(code=1)

    async def validation_flags_padding(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-p`.
        """
        print(
            bold(
                text="Error: You must correctly provide the numbers (int) `x` and `y` to apply the padding when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-p.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -p 5 5", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def validation_flags_cursor_shape(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-S`.
        """
        print(
            bold(
                text="Error: You must correctly provide one of the following values: Block | Underline | Beam when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-S.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -S Beam", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            italic(text="\t\tpycrypy -S Underline", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            italic(text="\t\tpycrypy -S Block", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def validation_flags_cursor_blinking(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-B`.
        """
        print(
            bold(
                text="Error: You must correctly provide one of the following values: Never | Off | On | Always when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-B.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -B Never", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            italic(text="\t\tpycrypy -B Off", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            italic(text="\t\tpycrypy -B On", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        print(
            italic(text="\t\tpycrypy -B Always", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    async def validation_flags_cursor_thickness(self: "Cli") -> None:
        """
        Prints a help message if a value is not correctly provided
        for the flag `-T`.
        """
        print(
            bold(
                text="Error: You must correctly provide the number (float) for the cursor thickness when using the option ",
                color="red",
            ),
            end="",
            flush=True,
            file=stderr,
        )
        print(italic(text="-T.", color="green"), end="\n", flush=True, file=stderr)
        print(
            bold(text="Usage example: ", color="cyan"), end="", flush=True, file=stderr
        )
        print(
            italic(text="pycrypy -T 0.3", color="white"),
            end="\n",
            flush=True,
            file=stderr,
        )
        return None

    # Retorna str o None
    async def execute(self: "Cli") -> Optional[str]:
        """
        This section of the code processes and validates the flags and arguments provided by the user to configure various options in Alacritty. Below are the steps performed:

        1. If the `--version` flag is provided, it prints the current version of pycrypy.
        2. Checks if the `alacritty.toml` file path exists; if not, it executes a verification function.
        3. Processes the `--theme` flag, formatting and applying the new theme.
        4. Processes the `--font` flag, setting the specified font.
        5. Processes the `--font-size` flag, setting the font size.
        6. Processes the `--style` flag, setting the font style.
        7. Processes the `--padding` flag, setting the padding.
        8. Processes the `--cursor-shape` flag, setting the cursor shape.
        9. Processes the `--cursor-blinking` flag, setting the cursor blinking behavior.
        10. Processes the `--opacity` flag, setting the window opacity.
        11. Processes the `--theme-path` flag, setting the theme path.
        12. Processes the `--cursor-thickness` flag, setting the cursor thickness.
        13. Processes the theme recommendation and configuration flags (`--theme-recommendations`, `--theme-dark`, `--theme-light`).
        14. If the `--verbose` flag is provided, it prints the list of verbose messages.

        Finally, it clears the temporary lists used to store light, dark, and recommended themes.
        """
        args: Namespace = await self.parse_args()
        verbose_list: List[str] = list()

        # Validamos si se proporciono un valor para la flag `t`
        if isinstance(args.theme, list) and len(args.theme) == 0:
            await self.validation_flags_theme(flag="t")
            exit(code=1)

        # Validamos si se proporciono un valor para la flag `P`
        if args.theme_path is None:
            await self.validation_flags_theme(flag="P")
            exit(code=1)

        # Verificamos si no se proporciono ningun valor para la flag `-f`
        if args.font is not None and not args.font:
            await self.validation_flags_font()
            exit(code=1)

        # Validamos si el valor proporcionado en la flag `-F` es de tipo float
        if args.fontSize is None:
            await self.validation_flags_font_size()
            exit(code=1)

        # Verificamos si no se proporciono ningun valor para la flag `-F`
        if args.fontSize is not None:
            args.fontSize = await self.cast_string_to_numeric(
                variable=args.fontSize, tipo=float
            )

        # Verificamos si no se proporciono ningun valor para la flag `-s`
        if args.style is not None and not args.style:
            await self.validation_flags_font_style()
            exit(code=1)

        # Verificamos si no se proporciono ningun valor para la flag `-o`
        if args.opacity is not None and not args.opacity:
            await self.validation_flags_opacity()
            exit(code=1)

        # Mapeamos a float y verficamos que el valor proporcionado es valido
        if args.opacity:
            args.opacity = await self.cast_string_to_numeric(
                variable=" ".join(args.opacity), tipo=float
            )

        # Verificamos si la el valor de la flag `-p` son de tipo int y tiene 2 valore x e y
        if args.padding is not None and len(args.padding) != 2:
            await self.validation_flags_padding()
            exit(code=1)

        if args.padding is not None and len(args.padding) == 2:
            s: int
            i: str
            for s, i in enumerate(iterable=args.padding, start=0):
                # s -> start: Para manejar el indice
                # i -> iterable: Para en cada iteracion tener el valor de un indice de la lista
                # await no puede ser incluido en una lambdafunción.
                args.padding[s] = await self.cast_string_to_numeric(
                    variable=i, tipo=int
                )

        # La primera condición verifica si la flag fue proporcionada por el usuario pero no se proporcionó ningún valor.
        # La segunda condición verifica que `args.cursorShape` no es una instancia de la clase bool,
        # lo que significa que la flag fue proporcionada por el usuario y tiene un valor.
        # La última condición valida que el valor proporcionado por el usuario,
        # después de aplicar el método title(), es uno de los valores permitidos: "Block", "Underline" o "Beam".
        if (
            args.cursorShape is None
            or not isinstance(args.cursorShape, bool)
            and args.cursorShape.title() not in ["Block", "Underline", "Beam"]
        ):
            await self.validation_flags_cursor_shape()
            exit(code=1)

        # La primera condición verifica si la flag fue proporcionada por el usuario pero no se proporcionó ningún valor.
        # La segunda condición verifica que `args.cursorShape` no es una instancia de la clase bool,
        # lo que significa que la flag fue proporcionada por el usuario y tiene un valor.
        # La última condición valida que el valor proporcionado por el usuario,
        # después de aplicar el método title(), es uno de los valores permitidos: "Never", "Off", "On" o "Always".
        if (
            args.cursor_blinking is None
            or not isinstance(args.cursor_blinking, bool)
            and args.cursor_blinking.title() not in ["Never", "Off", "On", "Always"]
        ):
            await self.validation_flags_cursor_blinking()
            exit(code=1)

        # Validamos si no se proporciono ningun valor al flag `-T`
        if args.cursor_thickness is None:
            await self.validation_flags_cursor_thickness()
            exit(code=1)

        # Validamos que el valor de la flag `-T` se pueda parsear a float
        if not isinstance(args.cursor_thickness, bool):
            args.cursor_thickness = await self.cast_string_to_numeric(
                variable=args.cursor_thickness, tipo=float
            )

        # Validamos que estas flags se usen simultaneamente
        if args.theme and args.theme_path:
            self.parser.error(
                bold(
                    text="Las opciones -t/--theme y -P/--theme-path no pueden usarse simultáneamente",
                    color="red",
                )
            )

        # * Procesamiento de las flags

        if args.version:
            print(await self.version_pycrypy(), end="\n", flush=True, file=stdout)

        # Verificar si la ruta del directorio de alacritty.toml existe
        directory_path: Path = Path(alacritty_toml_path)
        if not directory_path.exists():
            await verify_if_directory_exists(lista=verbose_list)

        # procesar los argumentos
        if args.theme:
            new_theme: str = " ".join(args.theme).lower()
            if " " in new_theme:
                new_theme = new_theme.replace(" ", "_")
            if "-" in new_theme:
                new_theme = new_theme.replace("-", "_")
            await load_new_theme(new_alacritty_theme=new_theme, lista=verbose_list)

        if args.font:
            await change_font(font_name=" ".join(args.font), lista=verbose_list)

        if isinstance(args.fontSize, float):
            await change_font_size(font_size=args.fontSize, lista=verbose_list)

        if args.style:
            await change_font_style(font_style=" ".join(args.style), lista=verbose_list)

        if args.padding:
            await change_padding(padding_list=args.padding, lista=verbose_list)

        if args.cursorShape and isinstance(args.cursorShape, str):
            await change_cursor_shape(
                shape_name=args.cursorShape.title(), lista=verbose_list
            )

        if args.cursor_blinking and isinstance(args.cursor_blinking, str):
            await change_cursor_blinking(
                blinking_name=args.cursor_blinking.title(), lista=verbose_list
            )

        if isinstance(args.opacity, float):
            await change_opacity(opacity=args.opacity, lista=verbose_list)

        if args.theme_path:
            await change_theme_path(theme_path=args.theme_path, lista=verbose_list)

        if isinstance(args.cursor_thickness, float):
            await change_cursor_thickness(
                cursor_thickness=args.cursor_thickness, lista=verbose_list
            )

        if args.theme_recommendations:
            await list_recommended_themes()
        if args.theme_dark:
            await list_dark_themes()
        if args.theme_light:
            await list_light_themes()

        if args.verbose:
            for i in verbose_list:
                print(i, end="\n", flush=True, file=stdout)

        # Borramos las lista que almacenanaban los modulos ya no son necesarios
        # del light_themes
        # del dark_themes
        # del recommended_themes

        return None
