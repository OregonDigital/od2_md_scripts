import json, yaml

data_struct = {
    "dmrec": {
        1: ["string", ""]
    }
}

with open("data_struct.json", "w") as jf:
    json.dump(data_struct, jf, indent=4)

with open("data_struct.yaml", "w") as yf:
    yaml.safe_dump(data_struct, yf)
