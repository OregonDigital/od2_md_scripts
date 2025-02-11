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
        """files_config() returs the paths entered in files_config.yaml.
        These are returned as a list: 
        [ 
            path_to_metadata.csv,
            path_to_files_directory 
        ]"""
        with open(self.filesconf, "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return [ paths['metadata'], paths['assets'] ]

    
    def default_config(self):
        with open(self.defaultconf, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
        return config
        

    def coll_config(self):
        with open(self.collconf, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
        return config


    def get_headers(self, metadata):
        with open(metadata, "r", encoding="utf-8-sig") as csvmetadata:
            reader = csv.DictReader(csvmetadata)
            headers = reader.fieldnames
        return headers


    # (!) needs further testing (!)
    # if pattern is in coll_config, I haven't figured out a way to 
    # make the compile arg a raw string...
    def check_identifier(self, csvfile, pattern): # add coll arg
        print(f"regex pattern to match: {pattern}\nMalformed values if any:") # add "for coll (...)"
        with open(csvfile, "r", encoding="utf-8-sig") as csvmetadata:
            reader = csv.DictReader(csvmetadata)
            p = re.compile(pattern) # this isn't a raw string... is that ok?
            malformed = []
            for row in reader:
                if not re.match(pattern, row['identifier']):
                    malformed.append(row['identifier'])
        return malformed


    def id_match_file(self, metadata): # uo-athletics
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

    # check_identifier, id_match_file *before* this step
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

