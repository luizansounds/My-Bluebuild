#!/bin/python3

import sys
import os
import subprocess as sp


if __name__ == "__main__":
    try:
        home_dir = os.getenv('HOME')
        config_dir = "/.config"
        themes_dir = f'{home_dir}/.themes'
        current_theme = sp.check_output("gsettings get org.gnome.desktop.wm.preferences theme", shell=True, universal_newlines=True)

        if "--reset" in sys.argv:
            print(f'==> Resetting theme to Adwaita\n')
            sp.run(["rm", f'{home_dir}{config_dir}/gtk-4.0/gtk.css'])
            sp.run(["rm", f'{home_dir}{config_dir}/gtk-4.0/gtk-dark.css'])
            sp.run(["rm", f'{home_dir}{config_dir}/gtk-4.0/assets'])
            sp.run(["rm", f'{home_dir}{config_dir}/assets'])
            sp.run(["gsettings", "set", "org.gnome.desktop.wm.preferences", "theme", "Adwaita"])
            sp.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", "Adwaita"])
            sp.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", "Adwaita"])
        else:
            all_themes = str(sp.run(["ls", f'{themes_dir}/'], stdout=sp.PIPE).stdout.decode("UTF-8")).split()        
            print(f"======== This script changes gtk4 theme from the installed themes in {themes_dir} =========")
            print("Select theme: ")
            for i, theme in enumerate(all_themes):
                print(f'{i+1}. {theme}')
            print("e. Exit")
            user_choice = input("Your choice: ")
            match user_choice:
                case "e":
                    print("Bye bye!")
                case _:
                    chosen_theme_idx = int(user_choice)-1
                    chosen_theme = all_themes[chosen_theme_idx]
                    print(f"==> Choosen theme: {chosen_theme}\n")
                    print(f"==> Removing previous theme: {current_theme}")
                    sp.run(["rm", f'{home_dir}{config_dir}/gtk-4.0/gtk.css'])
                    sp.run(["rm", f'{home_dir}{config_dir}/gtk-4.0/gtk-dark.css'])
                    sp.run(["rm", f'{home_dir}{config_dir}/assets'])
                    print(f"Installing {chosen_theme} theme...")
                    sp.run(["sudo", "flatpak", "override", f'--filesystem={home_dir}/.themes'])
                    sp.run(["ln", "-s", f'{themes_dir}/{chosen_theme}/gtk-4.0/gtk.css', f'{home_dir}{config_dir}/gtk-4.0/gtk.css'])
                    sp.run(["ln", "-s", f'{themes_dir}/{chosen_theme}/gtk-4.0/gtk-dark.css', f'{home_dir}{config_dir}/gtk-4.0/gtk-dark.css'])
                    sp.run(["ln", "-s", f'{themes_dir}/{chosen_theme}/assets', f'{home_dir}{config_dir}/assets'])                
                    sp.run(["gsettings", "set", "org.gnome.desktop.wm.preferences", "theme", f'{chosen_theme}'])
                    sp.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", f'{chosen_theme}'])
                    sp.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", f'{chosen_theme}'])
                    sp.run(["sudo", "flatpak", "override", f'--env=GTK_THEME={chosen_theme}'])
                    print("Done.")
    except ValueError as e:
        print("Incorrect value! Please try again!")
