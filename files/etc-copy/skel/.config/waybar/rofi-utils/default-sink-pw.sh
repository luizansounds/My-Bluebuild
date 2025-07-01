#!/bin/bash
#home/luiza/.config/waybar/rofi-utils/style-7.rasi

source /home/luiza/.ssd/extra/settings/dotfiles/waybar/rofi-utils/shared/theme-selector

# Create an associative array
declare -A sinks

# Get the list of sinks and their descriptions
sink_info=$(pactl list sinks)

# Retrieve the names and descriptions using sed
names=$(echo "$sink_info" | sed -n 's/.*Name: \(.*\)/\1/p')
descriptions=$(echo "$sink_info" | sed -n 's/.*Description: \(.*\)/\1/p')

# Populate the associative array
IFS=$'\n' read -r -d '' -a names_arr <<<"$names"
IFS=$'\n' read -r -d '' -a descriptions_arr <<<"$descriptions"

for ((i = 0; i < ${#descriptions_arr[@]}; i++)); do
    sinks["${descriptions_arr[$i]}"]="${names_arr[$i]}"
done

description=$(echo "$descriptions" | rofi -dmenu -p "Select Default Audio Sink" -theme ${dir}/${theme} )

if [ -n "${description}" ]; then
    pactl set-default-sink "${sinks[${description}]}" &&
        notify-send "Default Audio Sink" "${description}" ||
        notify-send "Couldn't set default audio sink!"
else
    echo "No sink selected. Default audio sink unchanged."
fi