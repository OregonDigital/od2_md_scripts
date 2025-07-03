import yaml, os, json, re
import pandas as pd

# to dos search "to do" + "duplicative codeblock"

class Package(object):

    def __init__(self, headers_config, test=False):
        # * instantiating with 1 vs 2 args ... any issues??
        # should I make sure that headers_config="test" when testing?
        self.test = test
        self.metadata = self.filepaths()[0]
        self.assets = os.listdir(self.filepaths()[1])
        self.default_config, self.headers_config = self.get_config(headers_config)
        # custom config requred, must include at least enumeration of headers
        # use makeconfig.py?

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
        print(f"(*i) metadata file path\n{self.metadata[0]}")
        try:
            print(f"(*i) Excel sheet/tab name\n{self.metadata[1]}")
        except:
            pass
        print(f"(*i) assets file path\n{self.filepaths()[1]}")

    def get_config(self, headers_config):
        with open("config/default.yaml", "r") as yf:
            default = yaml.safe_load(yf)
        with open(f"config/{headers_config}.yaml", "r") as yf:
            headers = yaml.safe_load(yf)
        return (default, headers,) # any different/better tuple vs. list here?

    def print_config(self):
        pretty = json.dumps(self.default_config, indent=4)
        print(f"*** default_config (JSON)\n{pretty}")
        pretty = json.dumps(self.headers_config, indent=4)
        print(f"*** headers_config (JSON)\n{pretty}")

    def metadata_file_type(self):
        if self.metadata[0].split('.')[-1] == "xlsx":
            return "Excel"
        elif self.metadata[0].split('.')[-1] == "csv":
            return "CSV"
        else:
            return "(!!) unknown metadata file type"
        
    def get_dataframe(self):
        if self.metadata_file_type() == "CSV" and isinstance(self.metadata, list):
            if len(self.metadata) != 1:
                print("(!!) for CSV, filepaths.yaml > metadata for CSV must be one-item list")
                exit()
            elif len(self.metadata) == 1:
                dataframe = pd.read_csv(self.metadata[0], dtype=str)
                return dataframe
            else:
                print("(!!) ERROR get_dataframe for CSV metadata")
        elif self.metadata_file_type() == "Excel" and isinstance(self.metadata, list):
            if len(self.metadata) < 1 or len(self.metadata) > 2:
                print("(!!) filenames.yaml > metadata for Excel must be one- or two-item list...")
                print("...with filepath, optionally sheet name (if no sheet name first sheet checked)")
                exit()
            elif len(self.metadata) == 1:
                dataframe = pd.read_excel(self.metadata[0], dtype=str)
                return dataframe
            elif len(self.metadata) == 2:
                dataframe = pd.read_excel(self.metadata[0], sheet_name=self.metadata[1], dtype=str)
                return dataframe
            else:
                print("(!!) ERROR get_dataframe for Excel metadata")
                exit()
        else:
            print("(!!) ERROR get_dataframe")
            exit()

    def get_headers(self):
        headers = self.get_dataframe().columns.to_list()
        return headers

    def print_headers(self):
        print("*** headers in metadata spreadsheet")
        for header in self.get_headers():
            print(header)

    def check_headers(self):
        check = True
        print("*** check headers configuration / headers in metadata")
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
            pass
        return check

    def perform_string_check(self, validation_data, instance_data, index):
        if str(validation_data) != str(instance_data):
            print(f"(!!) ERROR row {index + 2}: '{instance_data}' != string '{validation_data}'")

    def perform_regex_check(self, validation_data, instance_data, index):
        if not re.match(validation_data, instance_data):
            print(f"(!!) ERROR row {index + 2}: '{instance_data}' != {str(validation_data)}")

    def get_method(self, method_name, args):
        # see methods at bottom
        method_mapping = {
            'check_filenames_assets': self.check_filenames_assets,
            'identifier_file_match': self.identifier_file_match
            # more methods later?
        }
        try:
            method = method_mapping.get(method_name)
            if method:
                # print(f"method_mapping.get({method_name}) is True") # check
                return method(args)
            else:
                print(f"(!!) ERROR method_name {method_name} not in method_mapping")
        except Exception as e:
            print(f"(!!) get_method > try > except for '{method_name}': {e}")

    def select_data_for_checks(self, header, which, checktype, validation_data, args):
        df = self.get_dataframe()
        if checktype == 'regex':
            p = re.compile(r"{}".format(validation_data))
        if which == 'all':
            # duplicative codeblock 20250630B >
            for index, row in df.iterrows():
                if pd.notna(row[header]):
                    cell = row[header]
                else:
                    cell = ''
                for value in str(cell).split('|'):
                    if checktype == 'string':
                        self.perform_string_check(validation_data, value, index)
                    elif checktype == 'regex':
                        self.perform_regex_check(p, value, index)
                    else:
                        print("(!!) ERROR checktype arg passed to select_data_for_checks > which = all")
            # < end duplicative codeblock 20250630B
        elif which == 'complex':
            # duplicative codeblock 20250630B >
            for index, row in df.iterrows():
                if pd.notna(row[header]):
                    cell = row[header]
                else:
                    cell = ''
                try:
                    if row['format'] == 'https://w3id.org/spar/mediatype/application/xml':
                        # to do confirm / add this logic to documentation
                        for value in str(cell).split('|'):
                            if checktype == 'string':
                                self.perform_string_check(validation_data, value, index)
                            elif checktype == 'regex':
                                self.perform_regex_check(p, value, index)
                            else:
                                print("(!!) ERROR checktype arg passed to select_data_for_checks > which = complex")
                except:
                    print(f"(!!) ERROR metadata specified as complex object but no 'format' values")
            # < duplicative codeblock 20250630B
        elif which == 'item':
            # duplicative codeblock 20250630B >
            for index, row in df.iterrows():
                if pd.notna(row[header]):
                    cell = row[header]
                else:
                    cell = ''
                try:
                    if row.get('format') == None or row['format'] != 'https://w3id.org/spar/mediatype/application/xml':
                        # to do testing needed for this ^^^ logic
                        # to do confirm / add this logic to documentation
                        for value in str(cell).split('|'):
                            if checktype == 'string':
                                self.perform_string_check(validation_data, value, index)
                            elif checktype == 'regex':
                                self.perform_regex_check(p, value, index)
                            else:
                                print("(!!) ERROR checktype arg passed to select_data_for_checks > which = item")
                except:
                    print("(!!) ERROR metadata specified as complex-object item but has unexpected 'format' value")
            # < duplicative codeblock 20250630B
        elif which == 'na' and checktype == 'method':
            self.get_method(validation_data, args)
        else:
            print("(!!) ERROR 'blarf' select_data_for_checks")

    def get_headers_instructions(self):
        for header in self.headers_config:
            if self.headers_config[header] != None:
                print(f"*** check(s) for header '{header}' from headers config")
                for instruction in self.headers_config[header]:
                    # duplicative codeblock 20250630A
                    if instruction.get('string'):
                        print(f"*** *** string check for header '{header}' ({instruction['which']})")
                        self.select_data_for_checks(header, instruction['which'], 'string',
                                                    instruction['string'], None)
                    elif instruction.get('regex'):
                        print(f"*** *** regex check for header '{header}' ({instruction['which']})")
                        self.select_data_for_checks(header, instruction['which'], 'regex',
                                                    instruction['regex'], None)
                    elif instruction.get('method'):
                        print(f"*** *** method check ({instruction['method']}) for header '{header}'")
                        self.select_data_for_checks(header, 'na', 'method', instruction['method'], 
                                                    instruction['args'])
                    else:
                        print(f"(!!) ERROR unknown check type: headers_config '{header}' instruction {instruction}")
                    # duplicative codeblock 20250630A
            elif self.headers_config[header] == None:
                try:
                    if self.default_config[header] != None:
                        for instruction in self.default_config[header]:
                            print(f"*** check(s) for header '{header}' from default config")
                            # duplicative codeblock 20250630A
                            if instruction.get('string'):
                                print(f"*** *** string check for header '{header}' ({instruction['which']})")
                                self.select_data_for_checks(header, instruction['which'], 'string', 
                                                            instruction['string'], None)
                            elif instruction.get('regex'):
                                print(f"*** *** regex check for header '{header}' ({instruction['which']})")
                                self.select_data_for_checks(header, instruction['which'], 'regex', 
                                                            instruction['regex'], None)
                            elif instruction.get('method'):
                                print(f"*** *** method check ({instruction['method']}) for header '{header}'")
                                self.select_data_for_checks(header, 'na', 'method', instruction['method'], 
                                                            instruction['args'])
                            else:
                                print(f"(!!) ERROR unknown check type: default_config '{header}' instruction {instruction}")
                        # duplicative codeblock 20250630A
                    else:
                        print(f"(*i) NO CHECK CONFIGURED for header '{header}' in headers_ or default_config")
                except KeyError as e:
                    print(f"(*i) NO CHECK CONFIGURED for header {e} in headers_ or default_config")

    # methods for get_method
    # duplicative code here too in that I create and use dataframe separately for methods

    def check_filenames_assets(self, args):
        col = args[0]
        # print(f"args: {args}, type(args): {type(args)}") # check
        # print(f"col: {col}, type(col): {type(col)}") # check
        filenames = []
        for cell in self.get_dataframe()[col]:
            if pd.notna(cell):
                for value in str(cell).split('|'):
                    # print(value) # check
                    filenames.append(value)
        if set(filenames) != set(self.assets):
            print("(!!) ERROR set(filenames) != set(self.assets)")
            for filename in filenames:
                if filename not in self.assets:
                    print(f"(!!) {filename} not in files/ directory")
            for asset in self.assets:
                if asset not in filenames:
                    print(f"(!!) {asset} not in metadata filenames")
        else:
            pass

    def identifier_file_match(self, args):
        # (*i) NOTE this method only works with one filename, one identifier
        # print(f"args: {args}, type(args): {type(args)}") # check
        # print(f"args[0]: {args[0]}, type(args[0]): {type(args[0])}") # check
        substring = args[0]
        df_for_method = self.get_dataframe()
        # print(f"type(df_for_method): {type(df_for_method)}") # check
        for index, row in df_for_method.iterrows():
            if str(row['identifier']) == str(row['file']).replace(substring, ''):
                # print(f"{index + 2} OK") # check
                pass
            else:
                print(f"(!!) ERROR row {index + 2} '{row['identifier']} / '{row['file']}'")

    def save_as_csv(self):
        filename = self.filepaths[0].split('/')[-1]
        print(f"does filename == {filename}?")
