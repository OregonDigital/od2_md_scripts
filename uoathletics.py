import yaml, os, csv, re

class UOAIngest(object):


    def __init__(self):
        self.metadata = self.filepaths()[0]
        self.assets = os.listdir(self.filepaths()[1])
        self.config = self.fields_config()


    def filepaths(self):
        with open("filepaths.yaml", "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return [ paths['metadata'], paths['assets'] ]


    def fields_config(self):
        with open("config/uo-athletics_config.yaml", "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
            return(config)


    def csv_columns_processing(self):
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            for header in headers:
                # punting on file config, currently only config set as func
                if header in self.config and self.config[header] != None: # `~` in YAML
                    print(f"checking column {header}\n{'='*3}")
                    if self.config[header][0] == 'function':
                        pass
                    elif self.config[header][0] == 'string':
                        for row in reader:
                            if row[header] == self.config[header][1]:
                                pass
                            else:
                                print(f"correct value '{row[header]}'")
                    elif self.config[header][0] == 'regex':
                        for row in reader:
                            if not re.match(self.config[header][1], row[header]):
                                print(f"correct value {row[header]}")
                elif header in self.config and self.config[header] == None:
                    print(f"no check configured for header {header}\n{'='*3}")
                elif header not in self.config:
                    print(f"ERROR: {header} not in list of headers\n{'='*3}")
                else:
                    print("ERROR - some other unexpected error this is strange\n{'='*3}")


    def csv_filenames_assets_check(self):
        print(f"checking metadata filenames against files/ assets\n{'='*3}")
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            filenames = []
            for row in reader:
                filenames.append(row['file'])
            difflen = len(self.assets) - len(filenames)
            if difflen != 0:
                print("ERROR: # of filenames != # of asset files:")
                print(f"{len(filenames)} filename values in CSV metadata")
                print(f"{len(self.assets)} files in assets directory")
            else:
                print("# of filenames = # of asset files")
            # this check may still be wonky
            # (!) need to understand set better -- why am I using set here?
            # would diffs below work just as well with simple len() comparisons?
            diff = list(set(self.assets) - set(filenames))
            if len(diff) > 0:
                print(f"{len(diff)} files/ assets not in metadata\n{'*'*3}")
                for item in diff:
                    print(item)
                print("\n")
            else:
                print("files/ and metadata filenames match")
            diff = list(set(filenames) - set(self.assets))
            if len(diff) > 0:
                print(f"{len(diff)} filenames not in files/ assets\n{'*'*3}")
                for item in diff:
                    print(item)
                print("\n")
            else:
                print("metadata filenames and files/ match")
