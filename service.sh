#!/bin/bash
ALIAS_FILE="$HOME/.flatpak_aliases"
BASHRC_FILE="$HOME/.bashrc"
FLATPAK_ALIAS="main.py"

if [ ! -f "$ALIAS_FILE" ]; then
  touch "$ALIAS_FILE"
  echo "Created $ALIAS_FILE"
fi

if ! grep -q "source $ALIAS_FILE" "$BASHRC_FILE"; then
  echo "source $ALIAS_FILE" >>"$BASHRC_FILE"
  echo "Added source line to $BASHRC_FILE"
fi

if [ -f "$FLATPAK_ALIAS" ]; then
  python3 "$FLATPAK_ALIAS" --bashrc_file="$ALIAS_FILE" --remove all
  python3 "$FLATPAK_ALIAS" --bashrc_file="$ALIAS_FILE" --add all
  echo "Added Aliases to $ALIAS_FILE"
else
  echo "$FLATPAK_ALIAS does not exist."
fi

source "$BASHRC_FILE"
echo "Sourced $BASHRC_FILE"
