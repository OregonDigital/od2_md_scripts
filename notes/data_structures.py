import json, yaml

# don't like this one
# dsa = {
#     "dmrec": {
#         1: ["string", ""],
#         2: ["regex", "^$"]
#     }
# }

# ok yes use this one
dsb = {
    "dmrec": [
        {"string": ""},
        {"regex": "^$"}
    ]
    # to do how to pass method information here??
}

examples = {
    "dsb": dsb
}
for example in examples:
    with open(f"{example}.json", "w") as jf:
        json.dump(examples[example], jf, indent=4)
    with open(f"{example}.yaml", "w") as yf:
        yaml.safe_dump(examples[example], yf)
