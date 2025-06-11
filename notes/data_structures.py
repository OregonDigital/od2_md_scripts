import json, yaml

# don't like this one
# dsa = {
#     "dmrec": {
#         1: ["string", ""],
#         2: ["regex", "^$"]
#     }
# }

# ok yes use this one
structure_a = {
    "dmrec": [
        {"string": ""},
        {"regex": "^$"}
    ],
    "file": [
        {"method": ["check_filenames_assets"]} 
        # list is useless now but allow for passing 
        # args to methods after method name
    ]
}

examples = {"structure_a": structure_a}

for example in examples:
    with open(f"{example}.json", "w") as jf:
        json.dump(examples[example], jf, indent=4)
    with open(f"{example}.yaml", "w") as yf:
        yaml.safe_dump(examples[example], yf)
