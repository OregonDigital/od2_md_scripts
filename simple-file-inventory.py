"""
GPT 4.1
I'd like Python code to do the following as efficiently as possible.
Read in text file "simple-file-inventory.txt" and add each line (minus line ending) to a list. Each line is a directory file path.
For each directory file path in the list, do the following:
1. Get list of files in the directory, excluding subdirectories, then do one of the following (a or b):
a. if there is no .txt file in the directory having file name as [some date as YYYYMMDD]_[directory]_inventory.txt, create a .txt file with file name [date as YYYYMMDD]_[directory]_inventory.txt, including the following: at the top of the file, the date, the full directory file path (from simple-file-inventory.txt) and number of files in the directory. Following this after a separator, each file in the directory (excluding subdirectories) on a new line.
b. if there is a .txt file in the directory having file name as [some date as YYYYMMDD]_[directory]_inventory.txt, ask the user (y/n) if they would like to compare files currently in the directory against this inventory. If 'y', read in this text file and compare the list of files from step one with the files in the inventory following the separator, as described in a above. If there are any differences (different order is ok) show the user any differences in stdout, and ask (y/n) if they would like to save a new inventory file, with file name [date as YYYYMMDD]_[directory]_inventory.txt. If the sets are identical, indicate this to the user and exit without offering to save a new inventory file.
"""

import os
import sys
from datetime import datetime

INVENTORY_LIST_FILE = "simple-file-inventory.txt"
SEPARATOR = "---"

def read_inventory_list(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_files_in_directory(directory):
    try:
        return sorted([f for f in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, f))])
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
        return []

def get_inventory_filename(directory, date=None):
    dir_name = os.path.basename(os.path.normpath(directory))
    if date is None:
        # Find existing inventory files
        files = get_files_in_directory(directory)
        for f in files:
            if f.endswith(f"_{dir_name}_inventory.txt"):
                return f
        return None
    else:
        return f"{date}_{dir_name}_inventory.txt"

def write_inventory_file(directory, files, date):
    dir_name = os.path.basename(os.path.normpath(directory))
    filename = os.path.join(directory, f"{date}_{dir_name}_inventory.txt")
    with open(filename, "w") as f:
        f.write(f"{date}\n{directory}\n{len(files)}\n{SEPARATOR}\n")
        for file in files:
            f.write(f"{file}\n")
    print(f"Inventory file created: {filename}")

def read_inventory_file(filepath):
    with open(filepath, "r") as f:
        lines = [line.rstrip('\n') for line in f]
    try:
        sep_idx = lines.index(SEPARATOR)
        files = lines[sep_idx+1:]
        return set(files)
    except ValueError:
        print(f"Separator not found in {filepath}")
        return set()

def compare_and_report(current_files, inventory_files):
    current_set = set(current_files)
    inventory_set = set(inventory_files)
    only_in_current = current_set - inventory_set
    only_in_inventory = inventory_set - current_set
    if not only_in_current and not only_in_inventory:
        print("Directory matches inventory.")
        return True
    if only_in_current:
        print("Files only in directory:")
        for f in sorted(only_in_current):
            print(f"  {f}")
    if only_in_inventory:
        print("Files only in inventory:")
        for f in sorted(only_in_inventory):
            print(f"  {f}")
    return False

def main():
    if not os.path.exists(INVENTORY_LIST_FILE):
        print(f"Inventory list file '{INVENTORY_LIST_FILE}' not found.")
        sys.exit(1)
    directories = read_inventory_list(INVENTORY_LIST_FILE)
    today = datetime.now().strftime("%Y%m%d")
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Directory does not exist: {directory}")
            continue
        files = get_files_in_directory(directory)
        dir_name = os.path.basename(os.path.normpath(directory))
        # Find existing inventory file
        inventory_file = None
        for f in files:
            if f.endswith(f"_{dir_name}_inventory.txt"):
                inventory_file = os.path.join(directory, f)
                break
        if not inventory_file:
            # No inventory file, create one
            write_inventory_file(directory, files, today)
        else:
            ans = input(f"Inventory file found for '{directory}'. Compare with current files? (y/n): ").strip().lower()
            if ans != 'y':
                continue
            inventory_files = read_inventory_file(inventory_file)
            identical = compare_and_report(files, inventory_files)
            if identical:
                continue
            ans2 = input("Save new inventory file with current directory contents? (y/n): ").strip().lower()
            if ans2 == 'y':
                write_inventory_file(directory, files, today)

if __name__ == "__main__":
    main()

