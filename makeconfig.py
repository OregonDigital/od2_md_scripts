import csv, json, yaml, os
import pandas as pd

print("enter either (1) or (2)")
print("(1) absolute filepath to .csv metadata file, as:")
print(">>> C:\\Users\\briesenb\\Desktop\\metadata.csv")
print("(2) absolute filepath to .xlsx metadata file followed by space and sheet name, as:")
print(">>> C:\\Users\\briesenb\\Desktop\\metadata.xlsx Sheet1")

file = input(">>> ")

if len(file.split()) > 1 and file.split()[0].split('.')[-1] == "xlsx":
    filepath = file.split()[0]
    sheet_name = file.split()[1]
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    headers = df.columns.to_list()
elif len(file.split()) == 1 and file.split('.')[-1] == "csv":
    with open(file, "r", encoding="utf-8-sig") as csvf:
        reader = csv.reader(csvf)
        headers = next(reader)
else:
    print("(!) wrong number of input strings and/or unknown metadata file extension")
    exit()

config = {}
for entry in headers:
    config.update({entry: None})

# testing
# print(type(config))
# pretty = json.dumps(config, indent=4)
# print(pretty)
# with open("test.yaml", "w+") as yamlfile:
#     yaml.safe_dump(config, yamlfile, encoding="utf-8")

print("enter a name for your config file, excluding file extension, for example:")
print(">>> archival-materials")
print("enter 'n' to exit")

def get_input():
    user_input = input(">>> ")
    return user_input

filename = None

while filename is None:
    filename = get_input()
    if filename.lower() == 'n':
        exit()
    elif f"{filename}.yaml" in os.listdir("config"):
        print("a config file with that name already exists in od2_md_scripts/config/")
        filename = None
    elif filename == '':
        print("enter filename, or 'n' to exit")
        filename = None
    else:
        pass

print("(*) your config file will be created as follows:")
print(f"***path + file name: ../od2_md_scripts/config/{filename}.yaml")
print(f"***{len(config)} metadata fields (headers):")
for header in config:
    print(f"\t{header}")

while True:
    confirmation = input("proceed to create config template file? (y/n)\n>>> ").lower()
    if confirmation == 'y':
        with open(f"config/{filename}.yaml", "w+") as yamlfile:
            yaml.safe_dump(config, yamlfile, encoding='utf-8')
        print("config template ready:")
        print(f"od2_md_scripts/config/{filename}.yaml")
        break
    elif confirmation == 'n':
        break
    else:
        print("please enter 'y' or 'n'")
