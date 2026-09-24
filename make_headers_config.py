import csv, json, yaml, os, re
import pandas as pd
from typing import Optional, List
import utils

print("enter either (1) or (2)")
print("(1) absolute filepath to .csv metadata file, as:")
print(">>> C:\\Users\\briesenb\\Desktop\\metadata.csv")
print("(2) absolute filepath to .xlsx metadata file followed by space and sheet name, as:")
print(">>> C:\\Users\\briesenb\\Desktop\\metadata.xlsx Sheet1")

file_user_input = input(">>> ").strip()

if file_user_input.lower().endswith(".csv"):
    filepath = file_user_input
    # Treat the whole string as a path, so spaces are ok
    with open(filepath, "r", encoding="utf-8-sig") as csvf:
        reader = csv.reader(csvf)
        headers = next(reader)
else:
    # Expects [full xlsx path] [sheet name]
    # Checks right-most space, splits on it - this separates xlsx and sheet name (breaks if sheet name has space)
    parts = file_user_input.rsplit(" ", 1)
    # Checks first term is excel file, second term exists
    if len(parts) == 2 and parts[0].lower().endswith(".xlsx") and parts[1].strip():
        filepath, sheet_name = parts[0], parts[1].strip()
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        headers = df.columns.to_list()
    else:
        print("(!) expected either a .csv path, or: [xlsx path] [sheet name]")
        exit()

config = {}
for entry in headers:
    key = utils.base_header(entry)
    if key not in config:
        config[key] = None

print("enter a name for your config file, excluding file extension, for example:")
print("    >>> archival-materials")
print("names should not include spaces in them")
print("enter 'n' to exit")

def get_input() -> str:
    user_input = input(">>> ")
    return user_input

filename: Optional[str] = None

while filename is None:
    filename = get_input()
    if filename.lower() == 'n':
        exit()
    elif f"{filename}.yaml" in os.listdir("headers_fixes_config"):
        print("a config file with that name already exists in od2_md_scripts/headers_fixes_config/")
        filename = None
    elif filename == '':
        print("enter filename, or 'n' to exit")
        filename = None
    else:
        pass

print("(*) your config file will be created as follows:")
print(f"***path + file name: ../od2_md_scripts/headers_fixes_config/{filename}.yaml")
print(f"***{len(config)} metadata fields (headers):")
for header in config:
    print(f"\t{header}")

while True:
    confirmation = input("proceed to create config template file? (y/n)\n>>> ").lower()
    if confirmation == 'y':
        with open(f"headers_fixes_config/{filename}.yaml", "w+") as yamlfile:
            yaml.safe_dump(config, yamlfile, encoding='utf-8')
        print("config template ready:")
        print(f"od2_md_scripts/headers_fixes_config/{filename}.yaml")
        break
    elif confirmation == 'n':
        break
    else:
        print("please enter 'y' or 'n'")