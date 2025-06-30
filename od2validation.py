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
        print("\n")

    def get_config(self, headers_config):
        with open("config/default.yaml", "r") as yf:
            default = yaml.safe_load(yf)
        with open(f"config/{headers_config}.yaml", "r") as yf:
            headers = yaml.safe_load(yf)
        return [default, headers] # any different/better to use tuple here?

    def print_config(self):
        pretty = json.dumps(self.default_config, indent=4)
        print(f">>> default_config (JSON)\n{pretty}")
        pretty = json.dumps(self.headers_config, indent=4)
        print("\n")
        print(f">>> headers_config (JSON)\n{pretty}")
        print("\n")

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
        print("\n")

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
        print("\n")
        return check

    def report_validation_error(self):
        pass 
        # include index (row #) + header in error reporting
        # format (!!!) ERROR message

    # do I need func config error?

    def no_check_for_header(self, header):
        print(f"(*i*) NO CHECK CONFIGURED for header {header}")

    def perform_string_check(self, validation_data, instance_data, index):
        # print(f"""instance_data: type = {type(instance_data)}, {instance_data}, as string?
        #       {str(instance_data)}""") # check
        # OK I think I'm just going to have to convert pandas nan to '' manually in the check funcs...
        if pd.notna(instance_data):
            pass
        else:
            instance_data = ''
            print(f"after conversion instance data = '{instance_data}'")

    def perform_regex_check(self, validation_data, instance_data, index):
        # see note above re: converting pandas nan
        if pd.notna(instance_data):
            pass
        else:
            instance_data = ''
            print(f"after conversion instance data = '{instance_data}'")

    def get_method(self):
        print("blarf method checks not implemented yet")

    def check_filenames_assets(self):
        pass

    def identifier_file_match(self):
        pass

    def select_data_for_checks(self, header, instruction, checktype):
        # print(f"check {header} using {instruction}") # check
        df = self.get_dataframe()
        try:
            instruction.get('which')
            # print(f"for header {header}, perform checktype {checktype} on {instruction['which']} rows") # check
            if instruction['which'] == 'complex':
                # print(f"checking complex object rows for header {header}:") # check
                for index, row in df.iterrows():
                    if row['format'] == 'https://w3id.org/spar/mediatype/application/xml':
                        # print(index + 2) # check
                        # duplicative codeblock 20250630
                        if checktype == 'string':
                            self.perform_string_check(instruction['string'], row[header], index)
                        elif checktype == 'regex':
                            self.perform_regex_check(instruction['regex'], row[header], index)
                        elif checktype == 'method':
                            self.get_method()
                        else:
                            print("(!!!) something wrong with the checktype passed to select_data_for_checks")
                        # end duplicative codeblock 20250630
                    else:
                        pass
            elif instruction['which'] == 'item':
                # print(f"checking complex-object item rows for header {header}:") # check
                for index, row in df.iterrows():
                    if row['format'] != 'https://w3id.org/spar/mediatype/application/xml':
                        # print(index + 2) # check
                        # duplicative codeblock 20250630
                        if checktype == 'string':
                            self.perform_string_check(instruction['string'], row[header], index)
                        elif checktype == 'regex':
                            self.perform_regex_check(instruction['regex'], row[header], index)
                        elif checktype == 'method':
                            self.get_method()
                        else:
                            print("(!!!) something wrong with the checktype passed to select_data_for_checks")
                        # end duplicative codeblock 20250630
                    else:
                        pass
            else:
                print(f"(!!!) ERROR unknown 'which' in instruction {instruction}")
        except:
            # print(f"for header {header}, perform checktype {checktype} on all rows") # check
            # print(f"checking all rows for header {header}:") # check
            for index, row in df.iterrows():
                # print(index + 2) # check 
                # duplicative codeblock 20250630
                if checktype == 'string':
                    self.perform_string_check(instruction['string'], row[header], index)
                elif checktype == 'regex':
                    self.perform_regex_check(instruction['regex'], row[header], index)
                elif checktype == 'method':
                    self.get_method()
                else:
                    print("(!!!) something wrong with the checktype passed to select_data_for_checks")
                # end duplicative codeblock 20250630

    def get_header_instruction(self):
        for header in self.headers_config:
            # print(header) # check
            if self.headers_config[header] == None:
                # print(self.default_config[header]) # check
                try:
                    self.default_config[header]
                    if self.default_config[header] != None:
                        print(f">>> check(s) for header '{header}' from default config:")
                        for instruction in self.default_config[header]:
                            if instruction.get('string'):
                                checktype = 'string'
                            elif instruction.get('regex'):
                                checktype = 'regex'
                            elif instruction.get('method'):
                                checktype = 'method'
                            else:
                                print(f"(!!!) ERROR unknown check type in instruction {instruction}")
                            # print(instruction) # check
                            self.select_data_for_checks(header, instruction, checktype)
                    else:
                        self.no_check_for_header(header)
                except:
                    self.no_check_for_header(header)
            else:
                # print(self.headers_config[header]) # check
                print(f">>> check(s) for header {header} from headers config:")
                for instruction in self.headers_config[header]:
                    if instruction.get('string'):
                        checktype = 'string'
                    elif instruction.get('regex'):
                        checktype = 'regex'
                    elif instruction.get('method'):
                        checktype = 'method'
                    else:
                        print(f"(!!!) ERROR unknown check type in instruction {instruction}")
                    # print(instruction) # check
                    self.select_data_for_checks(header, instruction, checktype)
