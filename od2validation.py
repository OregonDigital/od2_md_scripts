import yaml, os, json, csv
import pandas as pd

class Package(object):

    def __init__(self, headers_config, test=False):
        # * instantiating with 1 vs 2 args ... any issues??
        # should I make sure that headers_config="test" when testing?
        self.test = test
        self.metadata = self.filepaths()[0]
        self.assets = os.listdir(self.filepaths()[1])
        self.default_config, self.headers_config = self.get_config(headers_config)
        # custom config requred, must include at least enumeration of headers
        # use makeconfig.py

    def filepaths(self):
        if self.test == False:
            with open("filepaths.yaml", "r") as yf:
                paths = yaml.safe_load(yf)
                return (paths['metadata'], paths['assets'],)
                # * self.metadata is 1 or 2 item list
        else:
            with open("filepaths_test.yaml", "r") as yf:
                paths = yaml.safe_load(yf)
                return (paths['metadata'], paths['assets'],)

    def print_filepaths(self):
        print(f">>> metadata file path\n{self.metadata[0]}")
        try:
            print(f">>> Excel sheet/tab name\n{self.metadata[1]}")
        except:
            pass
        print(f">>> assets file path\n{self.filepaths()[1]}")

    def get_config(self, headers_config):
        with open("config/default.yaml", "r") as yf:
            default = yaml.safe_load(yf)
        with open(f"config/{headers_config}.yaml", "r") as yf:
            headers = yaml.safe_load(yf)
        return [default, headers]

    def print_config(self):
        pretty = json.dumps(self.default_config, indent=4)
        print(f">>> default_config (JSON)\n{pretty}")
        pretty = json.dumps(self.headers_config, indent=4)
        print(f">>> headers_config (JSON)\n{pretty}")

    def metadata_file_type(self):
        if self.metadata[0].split('.')[-1] == "xlsx":
            return "Excel"
        elif self.metadata[0].split('.')[-1] == "csv":
            return "CSV"
        else:
            return "(!) unknown metadata file type"
        
    def get_dataframe(self):
        if self.metadata_file_type() == "CSV" and isinstance(self.metadata, list):
            if len(self.metadata) != 1:
                print("(!) for CSV, filepaths.yaml > metadata for CSV must be one-item list")
                exit()
            elif len(self.metadata) == 1:
                dataframe = pd.read_csv(self.metadata[0])
                return dataframe
            else:
                print("(!) ERROR get_dataframe for CSV metadata")
        elif self.metadata_file_type() == "Excel" and isinstance(self.metadata, list):
            if len(self.metadata) < 1 or len(self.metadata) > 2:
                print("(!) filenames.yaml > metadata for Excel must be one- or two-item list...")
                print("...with filepath, optionally sheet name (if no sheet name first sheet checked)")
                exit()
            elif len(self.metadata) == 1:
                dataframe = pd.read_excel(self.metadata[0])
                return dataframe
            elif len(self.metadata) == 2:
                dataframe = pd.read_excel(self.metadata[0], sheet_name=self.metadata[1])
                return dataframe
            else:
                print("(!) ERROR get_dataframe for Excel metadata")
                exit()
        else:
            print("(!) ERROR get_dataframe")
            exit()

    def get_headers(self):
        headers = self.get_dataframe().columns.to_list()
        return headers

    def print_headers(self):
        print(">>> headers in metadata spreadsheet")
        for header in self.get_headers():
            print(header)

    def check_headers(self):
        check = True
        print(">>> checking headers configuration / headers in metadata")
        if set(self.headers_config) != set(self.get_headers()):
            check = False
            print("!!! headers_config != metadata headers")
            diff = list(set(self.get_headers()) - set(self.headers_config))
            if len(diff) > 0:
                print("* metadata headers not in config file:")
                for item in diff:
                    print(item)
            diff = list(set(self.headers_config) - set(self.get_headers()))
            if len(diff) > 0:
                print("* headers_config fields not in metadata headers:")
                for item in diff:
                    print(item)
            print("* update metadata headers and/or headers_config and retry")
        else:
            print("* headers_config = metadata headers")
        return check

    def check_string(self):
        pass

    def check_regex(self):
        pass

    def get_method(self):
        pass

    def check_dataframe(self):
        for header in self.headers_config:
            print(f">>> check(s) for header {header}")
            # ah... here's where I need to add fallback to default.yaml (below)
            for check in self.headers_config[header]:
                if check.get("string"):
                    print(f"here is the string check data to use:\n{check}")
                elif check.get("regex"):
                    print(f"here is the regex check data to use:\n{check}")
                elif check.get("method"):
                    print(f"here is the method check to run")