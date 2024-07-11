#!/bin/bash

input_file="aliasflatpak.service.template"
output_file="aliasflatpak.service"
systemd_link="$HOME/.config/systemd/user/aliasflatpak.service"

current_user=$(whoami)
current_dir=$(pwd)

if [ ! "$EUID" -ne 0 ]; then
  echo "Please do not run as root or with sudo"
  exit 1
fi

sed -e "s/\$USER/$current_user/g" -e "s+\$WORKING_DIR+$current_dir+g" $input_file >$output_file

echo "Creating Link Between $current_dir/$output_file and $systemd_link"
sudo ln -s "$current_dir/$output_file" "$systemd_link"

echo "Service File saved as $output_file."
systemctl --user daemon-reload
systemctl --user --now enable $output_file

echo "Substitution complete. Service added to systemctl and started."
