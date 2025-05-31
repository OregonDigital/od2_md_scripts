import yaml, os, json, csv
import pandas as pd

class Package(object):

    def __init__(self, custom_config, test=False):
        # (!) additional arg may be having unexpected consequences
        # (!) do I fully understand how instantiating with 0, 1, 2 args works!?
        # TO DO 🦈: what to do about a custom config file?
            # if a check of headers is desired, some config file
            # specific to metadata spreadsheet is needed 🦈
        self.metadata = self.filepaths(test)[0]
        self.assets = os.listdir(self.filepaths(test)[1])
        self.default_config = self.get_config("default")
        self.custom_config = self.get_config(custom_config)

    def filepaths(self, test):
        if test == False:
            with open("filepaths.yaml", "r") as yf:
                paths = yaml.safe_load(yf)
                return (paths['metadata'], paths['assets'],)
                # (*) IMPORTANT change: metadata is now 1 or 2 item list
        else:
            with open("test/filepaths.yaml", "r") as yf:
                paths = yaml.safe_load(yf)
                return (paths['metadata'], paths['assets'],)

    def get_config(self, name):
        if name == None: # see 🦈
            return {}
        else:
            with open(f"config/{name}.yaml", "r") as yf:
                return yaml.safe_load(yf)

    def print_config(self):
        if self.custom_config == {}: # see 🦈
            print("(*) no custom config data")
        else:
            print("custom config data >>>\n")
            pretty = json.dumps(self.custom_config, indent=4)
            print(pretty)
        print("default config data >>>\n")
        pretty = json.dumps(self.default_config, indent=4)
        print(pretty)

    def metadata_file_type(self):
        if self.metadata[0].split('.')[-1] == "xlsx":
            return "Excel"
        elif self.metadata[0].split('.')[-1] == "csv":
            return "CSV"
        else:
            return "(!) unknown metadata file type"

    def check_headers(self):
        # WAIT how do you check headers unless you have a custom config file!?!?
        check = True
        if self.metadata_file_type() == "CSV":
            with open(self.metadata[0], "r", encoding="utf-8-sig") as csvf:
                reader = csv.reader(csvf)
                headers = next(reader) # type should == list
                pass # see 🦈 question above
        elif self.metadata_file_type() == "Excel":
            if isinstance(self.metadata, list):
                if len(self.metadata) <= 1:
                    print("filenames.yaml must include sheet name for Excel file")
                elif len(self.metadata) == 2:
                    md = pd.read_excel(self.metadata[0], sheet_name=self.metadata[1])
                    headers = md.columns.to_list() # type should == list
                    pass # see 🦈 question above
