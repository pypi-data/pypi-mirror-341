#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from asyncio import run
from cli import Cli
from sys import exit

def main() -> None:
    """
    Funcion Principal
    """
    args: Cli = Cli()
    run(main=args.execute())
    return None


if __name__ == "__main__":
    main()
    exit(0)
