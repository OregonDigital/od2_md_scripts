import csv, yaml, os

print("enter absolute filepath to .csv metadata file")
print("use forward slashes ('/'), not backslashes ('/')")
print("example:\nC:/Users/briesenb/Desktop/testfile.csv")

file = input(">>>")

with open(file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames

config = {}
for entry in headers:
    config.update({entry: None})

def get_config_name():
    print("enter a name for your config file, including the file extension '.yaml'")
    print("example:\narchival_materials.yaml")
    print("or, enter 'N' to abort")
    config_name = input(">>>")
    return config_name

filename = None
while filename == None:
    filename = get_config_name()
    if filename in os.listdir("config"):
        print("a config file with that name already exists in the config/ directory")
        filename = None
    elif filename.lower() == 'n':
        exit()
    else:
        pass

print("did this do what I thought it would?")
print(filename)
