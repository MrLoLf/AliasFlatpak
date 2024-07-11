#!/usr/bin/env python3

"""
Description: This program should addd aliases for flatpack apps that are installed on
             the system into the given file (defualt: .bashrc). To acces them via terminal easily.
Author: Fabian Roscher
License: MIT
"""

import subprocess
import os
import re
import argparse
import sys

def create_alias(aliases: dict[str, str], bashrc: str):
    """
    Creates an alias for a flatpak app and appends it to given file.

    Parameters:
    - alias_name (str): The name of the alias.
    - app_id (str): The ID of the flatpak app.
    - bashrc (str): The File to write aliases to

    Returns:
    None
    """
    print("Generating aliases for flatpak apps...")
    home_dir: str = os.path.expanduser('~')  # Get the home directory
    bashrc_path: str = os.path.join(home_dir, bashrc)  # Path to file
    with open(bashrc_path, 'r', encoding='UTF-8') as bashrc_file:  # Open in read mode
        existing_aliases: list[str] = bashrc_file.readlines()  # Read all existing aliases

    new_commands: list[str] = []
    for alias_name, app_id in aliases.items():
        command: str = f'alias {alias_name}="flatpak run {app_id}"\n'  # Alias command
        if command in existing_aliases:  # Check if the alias command already exists
            print(f"Alias '{alias_name}' for '{app_id}' already exists in {bashrc}.")
            continue
        new_commands.append(command)
        print(f"Alias '{alias_name}' for '{app_id}' will be added to {bashrc}.")

    if new_commands:
        with open(bashrc_path, 'a', encoding='UTF-8') as bashrc_file:  # Open in append mode
            bashrc_file.write(''.join(new_commands))  # Append the alias command to file
        print(f"Aliases added to {bashrc}.")

def remove_alias(alias_name: str, bashrc: str):
    """
    Removes an alias for a flatpak app from file.

    Parameters:
    - alias_name (str): The name of the alias.
    - bashrc (str): The File to remove alias from

    Returns:
    None
    """
    print("Removing alias for flatpak app...")
    home_dir: str = os.path.expanduser('~')  # Get the home directory
    bashrc_path: str = os.path.join(home_dir, bashrc)  # Path to file
    with open(bashrc_path, 'r', encoding='UTF-8') as bashrc_file:  # Open in read mode
        existing_aliases: list[str] = bashrc_file.readlines()  # Read all existing aliases

    removed: bool = False
    new_commands: list[str] = []
    for line in existing_aliases:
        if line.startswith(f'alias {alias_name}='):  # Check if the alias command exists
            removed = True
            print(f"Alias '{alias_name}' found in $(bashrc).")
        else:
            new_commands.append(line)

    if removed:
        with open(bashrc_path, 'w', encoding='UTF-8') as bashrc_file:  # Open in write mode
            bashrc_file.write(''.join(new_commands))  # Write the new alias commands to file
        print(f"Aliases removed from {bashrc}.")
    else:
        print(f"Alias '{alias_name}' not found in {bashrc}.")



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

def get_flatpak_apps() -> dict[str, str]:
    """
    Retrieves a dictionary of flatpak app aliases.

    Returns:
        A dictionary where the keys are the app aliases and the values are the app IDs.
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
            aliases["bitwarden"] = app_id
        elif app_id == "com.github.xournalpp.xournalpp":
            alias_name: str = "xournal"
            aliases["xournalpp"] = app_id
        elif app_id == "com.spotify.Client":
            alias_name: str = "sp"
            aliases["spotify"] = app_id
        else:
            # Replace spaces with hyphens for the alias name
            alias_name: str = format_alias_name(app_name)
        aliases[alias_name] = app_id

    if not aliases:
        print("No flatpak apps installed.")

    return aliases

def main():
    """
    Main function of the program. Runs the flatpak list command and
    parses the output to create aliases.

    Returns:
    None
    """

    parser = argparse.ArgumentParser(description="Manage flatpak app aliases.")
    parser.add_argument(
        '-a', '--add',
        type=str,
        help='Add a new alias for a flatpak app. With the name of the flatpak app as the argument.'\
    )
    parser.add_argument(
        '-r', '--remove',
        type=str,
        help='Remove an alias for a flatpak app. With the name of the alias as the argument.'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all app names for flatpak apps.'
    )
    parser.add_argument(
        "--bashrc_file",
        type=str,
        nargs='?',
        default=".bashrc",
        help="File to write aliases to. Defaults to \".bashrc\"")


    args = parser.parse_args()
    # Check if the user has provided any arguments
    if args.add is None and args.remove is None and not args.list:
        print("No arguments provided.")
        sys.exit(1)

    add_arg = None
    if args.add:
        add_arg = args.add.lower()

    remove_arg = None
    if args.remove:
        remove_arg = args.remove.lower()

    bashrc_file = None
    if args.bashrc_file:
        bashrc_file = args.bashrc_file


    aliases: dict[str, str] = get_flatpak_apps()

    special_aliases: dict[str, str] = {
        "bitwarden": "bw",
        "xournal": "xournal",
        "spotify": "sp"
    }

    if add_arg == "all":
        # Create aliases for all apps
        create_alias(aliases, bashrc_file)
    # Check if the user has entered a specific app to add an alias for
    elif add_arg in aliases:
        # check for special
        if add_arg in special_aliases:
            create_alias({special_aliases[add_arg]: aliases[add_arg]}, bashrc_file)
        create_alias({format_alias_name(add_arg): aliases[add_arg]}, bashrc_file)
    elif add_arg:
        print(f"App '{add_arg}' not found.")
    elif remove_arg == "all":
        # Remove all aliases
        for alias in aliases:
            remove_alias(alias, bashrc_file)
    elif remove_arg:
        remove_alias(remove_arg, bashrc_file)
    elif args.list:
        for alias, app_id in aliases.items():
            print(f"{alias}: {app_id}")


if __name__ == "__main__":
    main()
    print("Done! Please restart your terminal.")
