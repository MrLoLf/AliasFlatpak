# Description: This program should do aliases for flatpack apps that are installed on the system.
# Author: Fabian Roscher
# License: MIT

import subprocess
import os

def create_alias(alias_name :str , app_id: str):
    """
    Creates an alias for a flatpak app and appends it to .bashrc.

    Parameters:
    - alias_name (str): The name of the alias.
    - app_id (str): The ID of the flatpak app.

    Returns:
    None
    """
    home_dir = os.path.expanduser('~')  # Get the home directory
    bashrc_path = os.path.join(home_dir, '.bashrc')  # Path to .bashrc
    command = f'alias {alias_name}="flatpak run {app_id}"\n'  # Alias command
    with open(bashrc_path, 'a') as bashrc:  # Open .bashrc in append mode
        bashrc.write(command)  # Append the alias command to .bashrc

    print(f"Alias '{alias_name}' for '{app_id}' added to .bashrc. Please restart your terminal or source .bashrc to use it.")

def main():
    """
    Main function of the program.

    Returns:
    None
    """
    # Get the list of flatpak apps
    flatpak_list = subprocess.run(['flatpak', 'list'], capture_output=True, text=True, check=True).stdout

    # Parse the flatpak list and create aliases
    aliases = {}
    for line in flatpak_list.splitlines():
        parts = line.split()  # Split from the right to ensure only the last part is separated
        if len(parts) < 5:
            continue  # Ensure there are enough parts for app_name, app_id, version, channel, repo, and system
        app_id = parts[-5]  # app_id is now the fifth element from the end
        app_name = " ".join(parts[:-4]).split()[0]  # Reconstruct app_name by joining all parts except the last four and split them by space as they would double and take the first
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
        print(alias_name, app_id)
        aliases[alias_name] = app_id

    # Create aliases
    for alias, app_id in aliases.items():
        create_alias(alias, app_id)

if __name__ == "__main__":
    main()
