import yaml, os, csv, re

class Package(object):

    def __init__(self, coll="na", 
                filesconf="files_config.yaml",
                defaultconf="default_config.yaml",
                collconf="coll_config.yaml"):
        self = self
        self.coll = coll
        self.filesconf = filesconf
        self.defaultconf = defaultconf
        self.collconf = collconf


    def files_config(self):
        with open(self.filesconf, "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return [ paths['metadata'], paths['assets'] ]

    
    def get_headers(self, metadata):
        with open(metadata, "r", encoding="utf-8-sig") as csvmetadata:
            reader = csv.DictReader(csvmetadata)
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


    def default_config(self):
        with open(self.defaultconf, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
        return config
        

    def coll_config(self):
        with open(self.collconf, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
        return config


    def id_match_file(self, metadata):
        with open(metadata, "r", encoding="utf-8-sig") as csvmetadata:
            reader = csv.DictReader(csvmetadata)
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


    # (!) needs further testing (!)
    # is p.match doing exactly what I think it is?
    # IT ISNT
    def check_identifier(self, csvfile, pattern): # add coll arg
        print(f"regex pattern to match: {pattern}")
        with open(csvfile, "r", encoding="utf-8-sig") as csvmetadata:
            reader = csv.DictReader(csvmetadata)
            p = re.compile(r"{pattern}")
            malformed = []
            for row in reader:
                if not re.match(pattern, row['identifier']):
                    malformed.append(row['identifier'])
        if len(malformed) > 0:
            return f"CORRECT identifier values: {malformed}"
        else:
            return "identifier values match regex" # add "... for coll [collection]"

