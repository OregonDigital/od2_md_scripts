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

print("enter a name for your config file, including the file extension '.yaml', for example:")
print(">>>archival-materials.yaml")
print("enter 'n' to exit")

def get_input():
    user_input = input(">>>")
    return user_input

filename = None

while filename is None:
    filename = get_input()
    if filename.lower() == 'n':
        exit()
    elif filename in os.listdir("config"):
        print("a file with that name already exists in od2_md_scripts/config/")
        filename = None
    elif filename[-5:] != '.yaml':
        print("file name must include file extension '.yaml'")
        filename = None
    else:
        print("enter '[filename].yaml' or 'n' to exit")
        pass

print("(!) your config template file will be created as follows:")
print(f"***path + file name: od2_md_scripts/config/{filename}")
print(f"***metadata fields (headers) -- {len(config)} total:")
for header in config:
    print(f"\t{header}")

while True:
    confirmation = input("proceed to create config template file? (y/n)\n>>>").lower()
    if confirmation == 'y':
        jsonconfig = json.load(config)
        yaml.safe_load(jsonconfig)
        with open(f"config/{filename}", "w+") as yamlfile:
            yaml.safe_dump(jsonconfig)
        print("config template ready")
        break
    elif confirmation == 'n':
        break
    else:
        print("please enter 'y' or 'n'")
