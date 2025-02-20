# TODO
# Implement a catch function when no Steam Directory is placed
# Implement a user interaction field when program does its function

import os
import subprocess
import time
from tkinter import filedialog
from tkinter import Tk

# Steam Directory Functions

def get_steam_directory():
    root = Tk()
    root.withdraw()
    steam_folder = filedialog.askdirectory(title="Select your Steam folder")
    if steam_folder:
        print(f"Steam folder selected: {steam_folder}")
        return steam_folder
    else:
        print("No folder selected. Exiting...")
        exit()

steam_directory = get_steam_directory()

# Directory Paths

steam_executable = os.path.join(steam_directory, "steam.exe")
cfg_file_path = os.path.join(steam_directory, "steam.cfg")
steam_args = "-forcesteamupdate -forcepackagedownload -overridepackageurl http://web.archive.org/web/20240308104109if_/media.steampowered.com/client -exitsteam"

# Steam Close Process

def close_steam():
    print("Checking if Steam is running...")
    try:
        subprocess.run(["taskkill", "/IM", "steam.exe", "/F"], check=True)
        print("Steam is running, closing it...")
    except subprocess.CalledProcessError:
        print("Steam is not running.")

# Downgrade Steam

def downgrade_steam():
    close_steam()

    print("Downgrading steam...")

    command = [steam_executable] + steam_args.split()
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Steam exited with launched arguments, and should be updating.")

    if not os.path.exists(cfg_file_path):
        print("Creating steam.cfg to prevent updates...")
        with open(cfg_file_path, 'w') as cfg_file:
            cfg_file.write("BootStrapperInhibitAll=Enable")
    else:
        print("steam.cfg already exists, skipping creation.")
    
    print("Steam has been downgraded. Restart steam manually.")


# Upgrade Steam

def upgrade_steam():
    close_steam()

    if os.path.exists(cfg_file_path):
        print("Removing steam.cfg to allow Steam to update...")
        os.remove(cfg_file_path)
    else:
        print("steam.cfg file not found, no need to remove.")

    print("Launching Steam for update...")
    subprocess.run([steam_executable])

    print("Steam will now auto-update to the latest version")

# Main Menu

action = input("Do you want to downgrade or upgrade Steam? (Enter 'downgrade' or 'upgrade'): ").strip().lower()

if action == "downgrade":
    downgrade_steam()
elif action == "upgrade":
    upgrade_steam()
else:
    print("Invalid option. Please enter 'downgrade' or 'upgrade'.")


