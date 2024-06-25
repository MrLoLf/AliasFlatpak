# AliasFlatpak

## Table of Contents

- [AliasFlatpak](#aliasflatpak)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)

## Description

This project is designed to automatically create shell aliases for installed Flatpak applications, simplifying command-line usage and enhancing productivity.

## Installation

To use this project, follow these steps:

1. Clone the repository: `git clone https://github.com/MrLoLf/AliasFlatpak.git`
2. Navigate to the project directory: `cd AliasFlatpak`
3. Ensure Python 3.10 or higher is installed on your system.

## Usage

To use this project, follow these steps:

1. Run the script to generate aliases for all installed flatpak apps: `python main.py`
2. To generate an alias for a specific app, use the `--add` or `-a` flag followed by the app name. For example, to add an alias for Spotify: `python main.py --add spotify`
3. To remove an alias for a specific app, use the `--remove` or `-r` flag followed by the alias name. For example, to remove an alias for Spotify: `python main.py --remove spotify`
4. To list all current aliases, use the `--list` or `-l` flag: `python main.py --list`
5. Restart your terminal or source your shell configuration file (e.g., `source ~/.bashrc`) to apply the changes.

Examples:

```bash
# Generate aliases for all installed flatpak apps
python main.py --add all

# Generate an alias for a specific app (Spotify in this case)
python main.py --add spotify

# Remove an alias for a specific app (Spotify in this case)
python main.py --remove spotify

# List all current aliases
python main.py --list
```

Generating aliases for flatpak apps...
Done! Please restart your Terminal.

## Contributing

Contributions are welcome! Here's how you can contribute to this project:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.
