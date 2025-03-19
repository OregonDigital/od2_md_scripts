import csv, json, yaml, os

print("enter absolute filepath to .csv metadata file, for example:")
print(">>>C:\\Users\\briesenb\\Desktop\\metadata.csv")

file = input(">>>")

with open(file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames

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
print(">>>archival-materials")
print("enter 'n' to exit")

def get_input():
    user_input = input(">>>")
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

print("(!) your config template file will be created as follows:")
print(f"***path + file name: od2_md_scripts/config/{filename}")
print(f"***metadata fields (headers) -- {len(config)} total:")
for header in config:
    print(f"\t{header}")

while True:
    confirmation = input("proceed to create config template file? (y/n)\n>>>").lower()
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
