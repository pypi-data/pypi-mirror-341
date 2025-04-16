# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from io import TextIOWrapper

from setuptools import find_packages, setup

f: TextIOWrapper

with open(file=r"README.md", mode="r", encoding="utf-8") as f:
    README: str = f.read()

setup(
    name="pycrypy",
    version="1.0.0.alpha0",
    author="Daniel Benjamin Perez Morales",
    author_email="danielperezdev@proton.me",
    description="This utility, developed in Python3, significantly simplifies the configuration process of Alacritty, allowing easy adjustments to font, theme, padding, cursors, and font styles.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/D4nitrix13/pycrypy.git",
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # Indicates that packages are in "src"
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
    ],
    keywords="alacritty",
    python_requires=">=3.6",
    install_requires=[
        "altgraph>=0.17.4",
        "build>=1.2.2.post1",
        "certifi>=2025.1.31",
        "cffi>=1.17.1",
        "charset-normalizer>=3.4.1",
        "colored>=2.3.0",
        "cryptography>=44.0.2",
        "docutils>=0.21.2",
        "id>=1.5.0",
        "idna>=3.10",
        "jaraco.classes>=3.4.0",
        "jaraco.context>=6.0.1",
        "jaraco.functools>=4.1.0",
        "jeepney>=0.9.0",
        "keyring>=25.6.0",
        "markdown-it-py>=3.0.0",
        "mdurl>=0.1.2",
        "more-itertools>=10.6.0",
        "mypy>=1.15.0",
        "mypy-extensions>=1.0.0",
        "nh3>=0.2.21",
        "packaging>=24.2",
        "prettytable>=3.16.0",
        "pycparser>=2.22",
        "Pygments>=2.19.1",
        "pyinstaller>=6.12.0",
        "pyinstaller-hooks-contrib>=2025.2",
        "pyproject_hooks>=1.2.0",
        "readme_renderer>=44.0",
        "requests>=2.32.3",
        "requests-toolbelt>=1.0.0",
        "rfc3986>=2.0.0",
        "rich>=14.0.0",
        "SecretStorage>=3.3.3",
        "setuptools>=78.1.0",
        "toml>=0.10.2",
        "twine>=6.1.0",
        "types-toml>=0.10.8.20240310",
        "typing_extensions>=4.13.2",
        "urllib3>=2.4.0",
        "wcwidth>=0.2.13",
    ],
    include_package_data=True,
    entry_points=dict(console_scripts=["pycrypy = cli.main:main"]),
)
