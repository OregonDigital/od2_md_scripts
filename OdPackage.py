import yaml, os, csv

class Package:

    def __init__(self, config="files_config.yaml"):
        self = self
        self.config = config
    
    def get_files_md(self):
        with open(self.config, "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return (paths['metadata'], paths['assets'],)
    
    # this would be different for complex objects!
    # this only works for simple objects!!
    def check_assets_filenames(self, metadata, assets):
        assets_filenames = os.listdir(assets)
        filenames = []
        with open(metadata, "r", encoding="utf-8-sig") as csvmetadata:
            reader = csv.DictReader(csvmetadata)
            counter = 0
            for row in reader:
                counter += 1
                filenames.append(row['file'])
        difflen = len(assets_filenames) - len(filenames)
        if difflen != 0:
            print("ERROR: # of filenames != # of asset files:")
            print(f"{len(filenames)} filename values in CSV metadata")
            print(f"{len(assets_filenames)} files in assets directory")
        else:
            print("# of filenames = # of asset files")

        # still haven't checked values against values, only counts against counts
        # this is still wonky and duplicative?
        diff = list(set(assets_filenames) - set(filenames))
        if len(diff) > 0:
            print(f"{len(diff)} filenames from files/ not in metadata\n{'='*5}")
            for item in diff:
                print(item)
            print("\n")
        else:
            print("filenames in files/ and metadata match")
        
        diff = list(set(filenames) - set(assets_filenames))
        if len(diff) > 0:
            print(f"{len(diff)} filenames from metadata not in files/\n{'='*5}")
            for item in diff:
                print(item)
            print("\n")
        else:
            print("filenames in metadata and files/ match")

