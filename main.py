#!/usr/bin/env python3

"""
Description: This program should do aliases for flatpack apps that are installed on the system.
Author: Fabian Roscher
License: MIT
"""

import subprocess
import os

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

    new_commands = []
    for alias_name, app_id in aliases.items():
        command = f'alias {alias_name}="flatpak run {app_id}"\n'  # Alias command
        if command in existing_aliases:  # Check if the alias command already exists
            print(f"Alias '{alias_name}' for '{app_id}' already exists in .bashrc.")
            continue
        new_commands.append(command)
        print(f"Alias '{alias_name}' for '{app_id}'. Will be added to .bashrc.")

    if new_commands:
        with open(bashrc_path, 'a', encoding='UTF-8') as bashrc:  # Open .bashrc in append mode
            bashrc.write(''.join(new_commands))  # Append the alias command to .bashrc
        print("Aliases added to .bashrc.")

def main():
    """
    Main function of the program.

    Returns:
    None
    """
    # Get the list of flatpak apps
    flatpak_list = subprocess.run(['flatpak', 'list'],
                                  capture_output=True, text=True, check=True).stdout

    # Parse the flatpak list and create aliases
    aliases: dict[str, str] = {}
    for line in flatpak_list.splitlines():
        parts = line.split()  # Split from the right to ensure only the last part is separated
        if len(parts) < 2:
            # Ensure there are enough parts for app_name, app_id
            continue
        app_id = parts[1]  # app_id is now the fifth element from the end
        # Reconstruct app_name by joining all parts except the last four and split
        # them by space as they would double and take the first
        app_name = " ".join(parts[:-4]).split()[0]
        # Custom aliases for specific apps
        if app_id == "com.bitwarden.desktop":
            alias_name = "bw"
        elif app_id == "com.github.xournalpp.xournalpp":
            alias_name = "xournal"
        elif app_id == "com.spotify.Client":
            alias_name = "sp"
        else:
            # Create a general alias for other apps by using the first word of the app name
            alias_name = app_name.split()[0].lower()
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
