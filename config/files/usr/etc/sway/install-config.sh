#!/bin/bash

HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="Backtitle here"
TITLE="Install Pre-config"
MENU="Choose one of the following options:"

OPTIONS=(1 "Install W/ Flatpak"
         2 "Install W/o Flatpak"
         3 "Reboot"
         4 "Shutdown")

CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear
case $CHOICE in
        1)
            git -C ~/.local clone https://github.com/luizansounds/lu-dotfiles && sh ~/.local/lu-dotfiles/install.sh
            ;;
        2)
            git -C ~/.local clone https://github.com/luizansounds/lu-dotfiles && sh ~/.local/lu-dotfiles/install-no-flatpak.sh
            ;;

        3)
            rm /etc/sway/config && cp /usr/etc/sway/config.ini /etc/sway/config

        4)  
            systemctl reboot
            ;;
        5)
            systemctl poweroff
            ;;
esac
