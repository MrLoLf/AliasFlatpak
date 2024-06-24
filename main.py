#!/usr/bin/env python3

"""
Description: This program should addd aliases for flatpack apps that are installed on
             the system into the .bashrc file. To acces them via terminal easily.
Author: Fabian Roscher
License: MIT
"""

import subprocess
import os
import re

def create_alias(aliases: dict[str, str]):
    """
    Creates an alias for a flatpak app and appends it to .bashrc.

    Parameters:
    - alias_name (str): The name of the alias.
    - app_id (str): The ID of the flatpak app.

    Returns:
    None
    """
    home_dir: str = os.path.expanduser('~')  # Get the home directory
    bashrc_path: str = os.path.join(home_dir, '.bashrc')  # Path to .bashrc
    with open(bashrc_path, 'r', encoding='UTF-8') as bashrc:  # Open .bashrc in read mode
        existing_aliases: list[str] = bashrc.readlines()  # Read all existing aliases

    new_commands: list[str] = []
    for alias_name, app_id in aliases.items():
        command: str = f'alias {alias_name}="flatpak run {app_id}"\n'  # Alias command
        if command in existing_aliases:  # Check if the alias command already exists
            print(f"Alias '{alias_name}' for '{app_id}' already exists in .bashrc.")
            continue
        new_commands.append(command)
        print(f"Alias '{alias_name}' for '{app_id}'. Will be added to .bashrc.")

    if new_commands:
        with open(bashrc_path, 'a', encoding='UTF-8') as bashrc:  # Open .bashrc in append mode
            bashrc.write(''.join(new_commands))  # Append the alias command to .bashrc
        print("Aliases added to .bashrc.")

def format_alias_name(app_name: str) -> str:
    """Format the alias name for an application.

    This function takes an application name as input and formats it to be used as an alias.
    The formatting process involves keeping only alphanumeric characters and spaces, replacing
    spaces with hyphens, and converting the name to lowercase.

    Args:
        app_name (str): The name of the application.

    Returns:
        str: The formatted alias name.

    Example:
        >>> format_alias_name("My App Name")
        'my-app-name'
    """
    cleaned_name: str = re.sub(r'[^a-zA-Z0-9 ]', '', app_name)
    formatted_name: str = cleaned_name.replace(" ", "-").lower()
    return formatted_name

def main():
    """
    Main function of the program. Runs the flatpak list command and
    parses the output to create aliases.

    Returns:
    None
    """
    # Get the list of flatpak apps
    flatpak_list = subprocess.run(['flatpak', 'list'],
                                  capture_output=True, text=True, check=True).stdout

    # Parse the flatpak list and create aliases
    aliases: dict[str, str] = {}
    for line in flatpak_list.splitlines():
        # Split from the right to ensure only the last part is separated
        parts: list[str] = line.split()
        if len(parts) < 2:
            # Ensure there are enough parts for app_name, app_id
            continue

        # This regex captures two potential parts that could be the app ID
        match: re.Match[str] = re.search(
            r'([\w.-]+)\s+([\w.-]+)\s+([\w.-]+)\s+([\w.-]+)\s+system$', line
        )
        if not match:
            continue

        # Check which group looks more like an app ID (usually contains dots)
        app_id: str = match.group(2)
        if '.' in match.group(1):
            app_id: str = match.group(1)

        # Reconstruct app_name by joining all parts except the last five
        # if the app name contains spaces it's going to be blank so we
        # join all parts except the last four
        app_name: str = " ".join(parts[:-5])
        if not app_name:
            app_name: str = "".join(parts[:-4])
        # Custom aliases for specific apps
        if app_id == "com.bitwarden.desktop":
            alias_name: str = "bw"
        elif app_id == "com.github.xournalpp.xournalpp":
            alias_name: str = "xournal"
        elif app_id == "com.spotify.Client":
            alias_name: str = "sp"
        else:
            # Replace spaces with hyphens for the alias name
            alias_name: str = format_alias_name(app_name)
        aliases[alias_name] = app_id

    if not aliases:
        print("No flatpak apps installed.")
        return

    # Create aliases for all apps
    create_alias(aliases)

if __name__ == "__main__":
    print("Generating aliases for flatpak apps...")
    main()
    print("Done! Please restart your terminal.")
