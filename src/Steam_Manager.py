# TODO
# ~~Implement a catch function when no Steam Directory is placed~~
# ~~Implement a user interaction field when program does its functions~~
# ~~Implement a delay message feature??~~
# ~~Implement a catch function when there's a user input error on main menu~~
# ~~Implement a default File location check for Steam Directories~~

import os
import subprocess
import time
from tkinter import filedialog
from tkinter import Tk

def print_with_delay(message, delay=1):
    print(message)
    time.sleep(delay)

# Steam Directory Functions

def checkDefaultLocation():
    defaultPath = "C:/Program Files (x86)/Steam"
    if os.path.exists(os.path.join(defaultPath, "steam.exe")):
        return defaultPath
    return None

def get_steam_directory():
    while True:

        steam_folder = checkDefaultLocation()

        if steam_folder:
            print_with_delay(f"Default Steam folder found: {steam_folder}")
            return steam_folder
    
        root = Tk()
        root.withdraw()
        steam_folder = filedialog.askdirectory(title="Select your steam folder")

        if steam_folder:
            if os.path.exists(os.path.join(steam_folder, "steam.exe")):
                print_with_delay(f"Steam folder selected: {steam_folder}")
                return steam_folder
            else:
                print_with_delay(f"No steam.exe found in {steam_folder}. Please select a valid Steam file directory.")
                retry = input("Do you want to try again? (yes/no): ").strip().lower()
                
                if retry not in ["yes", "no"]:
                    print_with_delay("Invalid input. Please enter 'yes' or 'no'.")
                    continue
                
                if retry == "no":
                    print_with_delay("Exiting...")
                    exit()
        else:
            print_with_delay("No folder selected.")
            retry = input("Do you want to try again? (yes/no): ")

            if retry not in ["yes", "no"]:
                print_with_delay("Invalid input. Please enter 'yes' or 'no'.")
                continue

            if retry == "no":
                print_with_delay("Exiting...")
                exit()  

steam_directory = get_steam_directory()

# Directory Paths

steam_executable = os.path.join(steam_directory, "steam.exe")
cfg_file_path = os.path.join(steam_directory, "steam.cfg")
steam_args = "-forcesteamupdate -forcepackagedownload -overridepackageurl http://web.archive.org/web/20240308104109if_/media.steampowered.com/client -exitsteam"

# Steam Close Process

def close_steam():
    print_with_delay("Checking if Steam is running...")
    try:
        subprocess.run(["taskkill", "/IM", "steam.exe", "/F"], check=True)
        print_with_delay("Steam is running, closing it...")
    except subprocess.CalledProcessError:
        print_with_delay("Steam is not running.")

# Downgrade Steam

def downgrade_steam():
    close_steam()

    print_with_delay("Downgrading steam...")

    command = [steam_executable] + steam_args.split()
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print_with_delay(f"Steam exited with launched arguments, and should be updating.")

    if not os.path.exists(cfg_file_path):
        print_with_delay("Creating steam.cfg to prevent updates...")
        with open(cfg_file_path, 'w') as cfg_file:
            cfg_file.write("BootStrapperInhibitAll=Enable")
    else:
        print_with_delay("steam.cfg already exists, skipping creation.")
    
    print_with_delay("Steam has been downgraded. Restart steam manually.")

    input("Press any key to exit.")


# Upgrade Steam

def upgrade_steam():
    close_steam()

    if os.path.exists(cfg_file_path):
        print_with_delay("Removing steam.cfg to allow Steam to update...")
        os.remove(cfg_file_path)
    else:
        print_with_delay("steam.cfg file not found, no need to remove.")

    print_with_delay("Launching Steam for update...")
    subprocess.run([steam_executable])

    print_with_delay("Steam will now auto-update to the latest version")

    input("Press any key to exit.")

def get_valid_action():
    while True:
        action = input("Do you want to downgrade or upgrade steam? (Enter 'downgrade' or 'upgrade')")

        if action == "downgrade" or action == "upgrade":
            return action
        else:
            print("Invalid Option. Please enter 'downgrade' or 'upgrade'. Try Again")

# Main Menu

action = get_valid_action()

if action == "downgrade":
    downgrade_steam()
elif action == "upgrade":
    upgrade_steam()
else:
    print_with_delay("Invalid option. Please enter 'downgrade' or 'upgrade'.")


