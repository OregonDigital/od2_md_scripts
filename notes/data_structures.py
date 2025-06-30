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

# OK now expand example as follows:
# for any check, allow indication of check complex obj, or check item
structure_aplus = {
    "dmrec": [
        {"string": ""},
        {"regex": "^$"}
    ],
    "file": [
        {"method": "check_filenames_assets",
        # list is useless now but will allow for 
        # passing args to methods after method name
        "args": "",
        # this ^^^ should be optional
        "which": "item"
        # this ^^^ should be optional 
        }
    ],
    "title": [
        {"regex": "^Complex Object: .*$",
         "which": "complex"},
        {"regex": "^Complex Object Item: .*$",
         "which": "item"}
    ]
}

examples = {"a": structure_a,
            "aplus": structure_aplus}

for example in examples:
    with open(f"{example}.json", "w") as jf:
        json.dump(examples[example], jf, indent=4)
    with open(f"{example}.yaml", "w") as yf:
        yaml.safe_dump(examples[example], yf)
