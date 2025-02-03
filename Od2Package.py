import yaml, os, csv

class Package(object):

    def __init__(self, coll="na", 
                files_config="files_config.yaml",
                default_config="default_config.yaml",
                coll_config="coll_config.yaml"):
        self = self
        self.coll = coll
        self.files_config = files_config
        self.default_config = default_config
        self.coll_config = coll_config


    def get_files_md(self):
        with open(self.files_config, "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return [ paths['metadata'], paths['assets'] ]

    
    def get_headers(self, metadata):
        with open(metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
        return headers


    # this would be different for complex objects!
    # this only works for simple objects!!
    def check_assets_filenames(self, metadata, assets):
        print(f"checking metadata filenames against assets dir/ filenames:")
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
        print('='*5)


    def id_match_file(self, metadata):
        with open(metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            mismatch = []
            for row in reader:
                if row['identifier'] == row['file'].split('.')[0]:
                    pass
                else:
                    mismatch.append(row['identifier'])
        if len(mismatch) > 0:
            return mismatch
        else:
            return "identifier values = filenames - file extension"

