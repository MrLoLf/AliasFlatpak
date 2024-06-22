# AliasFlatpak

## Table of Contents

- [AliasFlatpak](#aliasflatpak)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Adding to Startup on Linux](#adding-to-startup-on-linux)
    - [Ubuntu](#ubuntu)
    - [Fedora](#fedora)
    - [Arch Linux](#arch-linux)
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

1. Run the script to generate aliases: `python main.py`
2. Restart your terminal or source your shell configuration file (e.g., `source ~/.bashrc`) to apply the changes.

Example:

```bash
python main.py
```

Generating aliases...
Done! Please add the following line to your .bashrc: source /path/to/generated_aliases.sh

## Adding to Startup on Linux

To add this project to the startup on Linux for different distributions, follow the instructions below:

### Ubuntu

1. Open the terminal.
2. Navigate to the project directory: `cd AliasFlatpak`
3. Edit your `.bashrc` or `.bash_profile` to run the script at login:

   ```bash
   echo "python /path/to/AliasFlatpak/main.py" >> ~/.bashrc
   ```

4. Reload your bash configuration: `source ~/.bashrc`

### Fedora

1. Open the terminal.
2. Navigate to the project directory: `cd AliasFlatpak`
3. Edit your `.bash_profile` to run the script at login:

   ```bash
   echo "python /path/to/AliasFlatpak/main.py" >> ~/.bashrc
   ```

4. Reload your bash profile: `source ~/.bash_profile`

### Arch Linux

1. Open the terminal.
2. Navigate to the project directory: `cd AliasFlatpak`
3. Edit your `.bashrc` or `.bash_profile` to run the script at login:

   ```bash
   echo "python /path/to/AliasFlatpak/main.py" >> ~/.bashrc
   ```

4. Reload your bash configuration: `source ~/.bashrc`

## Contributing

Contributions are welcome! Here's how you can contribute to this project:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.
