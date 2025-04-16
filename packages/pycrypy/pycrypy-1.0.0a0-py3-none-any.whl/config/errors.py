#!/usr/bin/env python3

# Author: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# Gitlab: https://gitlab.com/D4nitrix13
# Email: danielperezdev@proton.me

from lib.format_ansi_color import bold, italic


# Topic not found in the system: Abbreviated net
async def topic_not_found(name_topic: str) -> str:
    """
    Generates a formatted error message when a specific topic is not found in the system.

    Parameters:
    - name_topic (str): The name of the topic that was not found.

    Returns:
    - str: A formatted error message indicating that the topic was not found.

    Behavior:
    - Constructs an error message using bold and italic formatting.
    - `v1` contains the bold text "Error: Topic not found" with red color.
    - `v2` contains the topic name in italic and green color.
    - `v3` contains the bold text "in the system" with red color.
    - Returns the concatenation of `v1`, `v2`, and `v3`.

    Example usage:
    - If `topic_not_found(name_topic="unknownTopic")` is called, the function will return a formatted message indicating that the topic "unknownTopic" was not found in the system.
    """
    v1: str = bold(text="Error: Topic not found", color="red")
    v2: str = italic(text=f"`{name_topic}`", color="green")
    v3: str = bold(text="in the system", color="red")
    return v1 + v2 + v3
