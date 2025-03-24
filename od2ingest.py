import os, json, csv, re
import yaml

class Ingest(object):

    def __init__(self, config):
        self.metadata = self.filepaths()[0]
        self.assets = os.listdir(self.filepaths()[1])
        self.config = self.fields_config(config)

    def filepaths(self):
        with open("filepaths.yaml", "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return [ paths['metadata'], paths['assets'] ]

    def fields_config(self, config):
        with open(f"config/{config}.yaml", "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
            return(config)

    def check_config(self):
        pretty = json.dumps(self.config, indent=4)
        print(pretty)

    def check_columns_config(self):
        check = True
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            print(f"***checking config fields <> metadata headers")
            if set(self.config) != set(headers):
                check = False
                print("(!) ERROR config fields != metadata headers")
                diff = list(set(headers) - set(self.config))
                if len(diff) > 0:
                    print(f"headers not in config file:")
                    for item in diff:
                        print(item)
                diff = list(set(self.config) - set(headers))
                if len(diff) > 0:
                    print(f"config fields not in headers:")
                    for item in diff:
                        print(item)
                print("(!) UPDATE metadata headers or config, and retry")
            else:
                print("config fields = headers in metadata")
        return check
    
    def validation_error(self, header, data, check_type, check_data):
        print(f"(!) '{header}' ERROR: '{data}' does not match {check_type} {check_data}")
    
    def config_error(self, header, check_type, check_data):
        print(f"(*) CHECK column '{header}', or fix broken config '{check_type}', '{check_data}'")

    def get_method(self, header, check_type, check_data):
        method_mapping = {
            "check_filenames_assets": self.check_filenames_assets,
            "id_match_file": self.id_match_file
        }
        method = method_mapping.get(check_data)
        if method:
            return method()
        else:
            self.config_error(header, check_type, check_data)

    def process_columns(self):
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
        
        for key, value in self.config.items():
            header = key
            try: # fall back to default config would happen around here?
                check_type = value[0]
                check_data = value[1]
                print(f"***running {check_type} check for column '{header}'")
                if check_type == 'method':
                    self.get_method(header, check_type, check_data) 
                elif check_type == 'regex':
                    p = re.compile(r"{}".format(check_data))
                    for row in rows:
                        if not re.match(p, row[header]):
                            self.validation_error(header, row[header], check_type, check_data)
                elif check_type == 'string':
                    for row in rows:
                        if row[header] != str(check_data):
                            self.validation_error(header, row[header], check_type, check_data)
                else:
                    self.config_error(header, check_type, check_data)
                    print(f"(*) CHECK column '{header}', or fix broken config '{check_type}', '{check_data}'")
            except TypeError as e:
                print(f"(*) CHECK column '{header}': no check configured for this column")

    def check_filenames_assets(self):
        print(f">>>method: checking metadata filenames against files/ assets")
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            filenames = []
            for row in reader:
                filenames.extend(row['file'].split('|'))
            difflen = len(self.assets) - len(filenames)
            if difflen != 0:
                print("(!) ERROR: # of filenames != # of asset files:")
                print(f"{len(filenames)} filename values in CSV metadata")
                print(f"{len(self.assets)} files in assets directory")
            else:
                print("# of filenames = # of asset files")
            diff = list(set(self.assets) - set(filenames))
            if len(diff) > 0:
                print(f"*{len(diff)} files/ assets not in metadata:")
                for item in diff:
                    print(item)
            else:
                print("files/ and metadata filenames match")
            diff = list(set(filenames) - set(self.assets))
            if len(diff) > 0:
                print(f"*{len(diff)} filenames not in files/ assets:")
                for item in diff:
                    print(f"'{item}'")
            else:
                print("metadata filenames and files/ match")
 
    def id_match_file(self):
        # uo-athletics
        # (!) DOES NOT account for multiple file names in single cell
        # to-do ingegrate function calls into config, so function can be called for row
        print(">>>method: checking for id / file value matches")
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            # print(rows)
            mismatch = []
            for row in rows:
                if row['file'].split('.')[0] == row["identifier"]:
                    pass
                else:
                    mismatch.append(f"file '{row['file']}' != identifier '{row['identifier']}'")
        if len(mismatch) > 0:
            for item in mismatch:
                print(f"(!) ERROR: {item}")
        else:
            return "identifier values = filenames - file extension"
