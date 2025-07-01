import json, yaml

config_data_structure = {
    "dmrec": [
        {"string": "",
         "which": "all"},
        {"regex": "^$",
         "which": "all"}
    ],
    "file": [
        {"method": "check_filenames_assets",
        # list is useless now but will allow for 
        # passing args to methods after method name
        "args": [],
        }
    ],
    "title": [
        {"regex": "^Complex Object: .*$",
         "which": "complex"},
        {"regex": "^Complex Object Item: .*$",
         "which": "item"}
    ]
}

with open(f"config_data_structure.json", "w") as jf:
    json.dump(config_data_structure, jf, indent=4)
with open(f"config_data_structure.yaml", "w") as yf:
    yaml.safe_dump(config_data_structure, yf)
