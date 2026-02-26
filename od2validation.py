import yaml, os, json, re
import pandas as pd
import logging
from typing import Tuple, List, Dict, Any, Optional, Pattern
import vocabularies
import copy

# Logger replaces print statements for debugging/usage
# (It basically controls the level of info to print)
logger = logging.getLogger(__name__)

# to dos search "to do" + "duplicative codeblock"

class Package(object):

    def __init__(self, headers_config: str, test: bool = False) -> None:
        # * instantiating with 1 vs 2 args ... any issues??
        # should I make sure that headers_config="test" when testing?
        self.test = test
        self.metadata = self.filepaths()[0]
        self.assets = os.listdir(self.filepaths()[1])
        self.default_config, self.headers_config, self.validation_mappings = self.get_config(headers_config)
        self.validator_mapping = self._build_validator_mapping()
        # custom config requred, must include at least enumeration of headers
        # use makeconfig.py?

    def filepaths(self) -> Tuple[List[str], str]:
        if self.test == False:
            with open("filepaths.yaml", "r") as yf:
                paths: Dict[str, Any] = yaml.safe_load(yf)
                return (paths['metadata'], paths['assets'],)
                # * self.metadata is 1 or 2 item list
        else:
            with open("filepaths_test.yaml", "r") as yf:
                paths: Dict[str, Any] = yaml.safe_load(yf)
                return (paths['metadata'], paths['assets'],)

    def _build_validator_mapping(self) -> Dict[str, str]:
        """Build mapping: field_name -> validator_name"""
        mapping = {}
        for validator_name, fields in self.validation_mappings.get('field_validators', {}).items():
            for field in fields:
                mapping[field.lower()] = validator_name
        return mapping
    
    def print_filepaths(self) -> None:
        logger.info(f"metadata file path\n{self.metadata[0]}")
        try:
            logger.info(f"Excel sheet/tab name\n{self.metadata[1]}")
        except:
            pass
        logger.info(f"assets file path\n{self.filepaths()[1]}")

    def get_config(self, headers_config: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        with open("config/default.yaml", "r") as yf:
            default: Dict[str, Any] = yaml.safe_load(yf)
        with open(f"config/{headers_config}.yaml", "r") as yf:
            headers: Dict[str, Any] = yaml.safe_load(yf)
        with open("config/validation_mappings.yaml", "r") as yf:
            mappings: Dict[str, Any] = yaml.safe_load(yf)
        return (default, headers, mappings) # any different/better tuple vs. list here?

    def print_config(self) -> None:
        formatted_default: str = json.dumps(self.default_config, indent=4)
        logger.info(f"default_config (JSON)\n{formatted_default}")
        formatted_headers = json.dumps(self.headers_config, indent=4)
        logger.info(f"headers_config (JSON)\n{formatted_headers}")

    def metadata_file_type(self) -> str:
        if self.metadata[0].split('.')[-1] == "xlsx":
            return "Excel"
        elif self.metadata[0].split('.')[-1] == "csv":
            return "CSV"
        else:
            logger.error("unknown metadata file type")
            return "unknown metadata file type"
        
    def get_dataframe(self) -> pd.DataFrame:
        if self.metadata_file_type() == "CSV" and isinstance(self.metadata, list):
            if len(self.metadata) != 1:
                logger.error("for CSV, filepaths.yaml > metadata for CSV must be one-item list")
                exit()
            elif len(self.metadata) == 1:
                dataframe: pd.DataFrame = pd.read_csv(self.metadata[0], dtype=str)
                return dataframe
            else:
                logger.error("get_dataframe for CSV metadata")
        elif self.metadata_file_type() == "Excel" and isinstance(self.metadata, list):
            if len(self.metadata) < 1 or len(self.metadata) > 2:
                logger.error("filenames.yaml > metadata for Excel must be one- or two-item list...")
                logger.error("...with filepath, optionally sheet name (if no sheet name first sheet checked)")
                exit()
            elif len(self.metadata) == 1:
                dataframe: pd.DataFrame = pd.read_excel(self.metadata[0], dtype=str)
                return dataframe
            elif len(self.metadata) == 2:
                dataframe: pd.DataFrame = pd.read_excel(self.metadata[0], sheet_name=self.metadata[1], dtype=str)
                return dataframe
            else:
                logger.error("get_dataframe for Excel metadata")
                exit()
        else:
            logger.error("get_dataframe")
            exit()

    def get_headers(self) -> List[str]:
        headers: List[str] = self.get_dataframe().columns.to_list()
        return headers

    def print_headers(self) -> None:
        logger.info("headers in metadata spreadsheet")
        for header in self.get_headers():
            logger.info(header)

    def check_headers(self) -> bool:
        check: bool = True
        logger.info("check headers configuration / headers in metadata")
        if set(self.headers_config) != set(self.get_headers()):
            check = False
            logger.error("headers_config != metadata headers")
            diff: List[str] = list(set(self.get_headers()) - set(self.headers_config))
            if len(diff) > 0:
                logger.info("metadata headers not in config file:")
                for item in diff:
                    logger.error("  %s", item)
            diff: List[str] = list(set(self.headers_config) - set(self.get_headers()))
            if len(diff) > 0:
                logger.error("headers_config fields not in metadata headers:")
                for item in diff:
                    logger.error("  %s", item)
            logger.error("update metadata headers and/or headers_config and retry")
        else:
            pass
        return check

    def perform_string_check(self, validation_data: Any, instance_data: Any, index: int) -> None:
        if str(validation_data) != str(instance_data):
            logger.error(f"row {index + 2}: '{instance_data}' != string '{validation_data}'")
    
    def perform_regex_check(self, validation_data: Pattern[str], instance_data: str, index: int) -> None:
        if not re.match(validation_data, instance_data):
            logger.error(f"row {index + 2}: '{instance_data}' does not match regex for header values")

    def get_method(self, method_name: str, args: Optional[List[Any]]) -> Optional[Any]:
        # see methods at bottom
        method_mapping = {
            'check_filenames_assets': self.check_filenames_assets,
            'identifier_file_match': self.identifier_file_match,
            'validate_controlled_vocab': self.validate_controlled_vocab
            # more methods later?
        }
        try:
            method: Optional[Any] = method_mapping.get(method_name)
            if method:
                logging.debug(f"method_mapping.get({method_name}) is True")
                return method(args)
            else:
                logger.error(f"method_name {method_name} not in method_mapping")
        except Exception as e:
            logger.error(f"get_method > try > except for '{method_name}': {e}")

    def _validate_cell_values(self, df: pd.DataFrame, header: str, validation_data: Any, 
                              checktype: str, p: Optional[Pattern[str]] = None) -> None:
        """
        Validates cell values in a dataframe column.
        Works by:

        1. Iterates through each row in dataframe
        2. Gets cell value or empty string if missing
        3. Splits multi-value cells on '|'
        4. Validates each value using string or regex check
        """
        for index, row in df.iterrows():
            # Get cell value and convert missing values to empty string
            if pd.notna(row[header]):
                cell = row[header]
            else:
                cell = ''

            # Split on '|' for multi-value cells and validate each value
            for value in str(cell).split('|'):
                if checktype == 'string':
                    self.perform_string_check(validation_data, value, index)
                elif checktype == 'regex' and p is not None:
                    self.perform_regex_check(p, value, index)
                else:
                    logger.error(f"Unkown checktype '{checktype}' in  _validate_cell_values")

    def select_data_for_checks(self, header: str, which: str, checktype: str, validation_data: Any, args: Optional[List[Any]]) -> None:
        df: pd.DataFrame = self.get_dataframe()
        
        # Compile regex pattern
        # TODO: verify pattern is actually the right thing to use here (p: Pattern[str]) for type hint
        p = re.compile(r"{}".format(validation_data))

        if which == 'all':
            # Validate all rows without filtering
            self._validate_cell_values(df, header, validation_data, checktype, p)

        elif which == 'complex':
            # Only validate rows with format column that has XML (complex object)
            try:
                complex_df: pd.DataFrame = df[df['format'] == 'https://w3id.org/spar/mediatype/application/xml']
                self._validate_cell_values(complex_df, header, validation_data, checktype, p)
            except KeyError:
                logger.error(f"metadata specified as complex object but no 'format' column exists")

        elif which == 'item':
                # Only validate rows where format is missing or not XML (simple item)
                try:
                    # Filter to rows where format is NaN or not XML
                    item_df: pd.DataFrame = df[(df['format'].isna()) | 
                                 (df['format'] != 'https://w3id.org/spar/mediatype/application/xml')]
                    self._validate_cell_values(item_df, header, validation_data, checktype, p)
                except KeyError:
                    logger.error("metadata specified as complex-object item but has unexpected 'format' value")

        elif which == 'na' and checktype == 'method':
            # Run custom method, not standard validation
            self.get_method(validation_data, args)
        else:
            logger.error(f"Invalid 'which' parameter: {which}. Expected 'all', 'complex', 'item', or 'na'.")

    def _process_instructions(self, header: str, instructions: List, config_source: str) -> None:
        """
        Process validation instructions for a specific header

        Iterates through list of validation instructions and executes check (string, regex, or method) for each instruction

        Args:
            header: Column name being validated
            instructions: List of instruction dicts (which hold validation type and parameters)
            config_source: Name of config file for error logging
        """
        for instruction in instructions:
            if instruction.get('string'):
                logger.debug(f"string check for header '{header}' ({instruction['which']})")
                self.select_data_for_checks(header, instruction['which'], 'string',
                                            instruction['string'], None)
            elif instruction.get('regex'):
                logger.debug(f"regex check for header '{header}' ({instruction['which']})")
                self.select_data_for_checks(header, instruction['which'], 'regex',
                                            instruction['regex'], None)
            elif instruction.get('method'):
                logger.debug(f"method check ({instruction['method']}) for header '{header}'")
                self.select_data_for_checks(header, 'na', 'method', instruction['method'], 
                                            instruction['args'])
            else:
                logger.error(f"unknown check type: {config_source} '{header}' instruction {instruction}")

    def _update_method_args(self, instructions: List, old_name: str, new_name: str) -> List:
        """
        Update method args in instructions to use actual header name instead of validator type name

        Args:
            instructions: List of instruction dicts
            old_name: Original validator type name (e.g., 'creator')  
            new_name: Actual header name (e.g., 'photographer')

        Returns:
            Modified copy of instructions with updated args
        """
        updated_instructions = copy.deepcopy(instructions)
        for instruction in updated_instructions:
            if instruction.get('method') and instruction.get('args'):
                # Replace old_name with new_name in args
                instruction['args'] = [new_name if arg == old_name else arg for arg in instruction['args']]
        return updated_instructions

    def get_headers_instructions(self) -> None:
        """
        Decide validation instructions for config files headers

        For each header in headers_config:
        1. If header has validation rules in headers_config, use those
        2. If header is None in headers_config:
           a. Check validation_mappings for mapped validator (e.g., photographer->creator)
           b. Fallback to direct header lookup in default_config (e.g., dmrec)
        3. If header isn't in either config, log no check configured
        """
        for header in self.headers_config:
            # Use project-specific config if possible
            if self.headers_config[header] != None:
                logger.info(f"Validating '{header}' from config...")
                self._process_instructions(header, self.headers_config[header], 'headers_config')
            # Use default config if no project-specific config
            elif self.headers_config[header] is None:
                # Try mapped validator first (e.g., photographer->creator)
                validator_type = self.validator_mapping.get(header.lower())
                if validator_type and validator_type in self.default_config:
                    logger.info(f"Validating '{header}' from default config (mapped to '{validator_type}')...")
                    # Replace validator_type with actual header name in method args
                    instructions = self._update_method_args(self.default_config[validator_type], validator_type, header)
                    self._process_instructions(header, instructions, 'default')
                # Fallback to direct header name in default_config
                elif header in self.default_config and self.default_config[header] is not None:
                    logger.info(f"Validating '{header}' from default config...")
                    self._process_instructions(header, self.default_config[header], 'default')
                else:
                    logger.info(f"NO VALIDATION CHECK CONFIGURED FOR '{header}' in headers_config or default")
            else:
                logger.info(f"NO VALIDATION CHECK CONFIGURED FOR '{header} in headers_config or default")

    # methods for get_method
    # duplicative code here too in that I create and use dataframe separately for methods
    # TODO: condense dataframe usage, one declaration possible in init?
    
    def check_filenames_assets(self, args: List[Any]) -> None:
        col: str = args[0]
        filenames: List[str] = []
        for cell in self.get_dataframe()[col]:
            if pd.notna(cell):
                for value in str(cell).split('|'):
                    filenames.append(value)
        if set(filenames) != set(self.assets):
            logger.error("set(filenames) != set(self.assets)")
            for filename in filenames:
                if filename not in self.assets:
                    logger.error(f"'{filename}' not in files/ directory")
            for asset in self.assets:
                if asset not in filenames:
                    logger.error(f"'{asset}' not in metadata filenames")
        else:
            pass

    def identifier_file_match(self, args: List[str]) -> None:
        substring: str = args[0]
        df_for_method: pd.DataFrame = self.get_dataframe()
        for index, row in df_for_method.iterrows():
            if str(row['identifier']) == str(row['file']).replace(substring, ''):
                pass
            else:
                logger.error(f"row {index + 2} '{row['identifier']} / '{row['file']}'")

    def save_as_csv(self) -> None:
        filename: str = self.filepaths[0].split('/')[-1]
        logger.debug(f"does filename == {filename}?")
    
    def validate_controlled_vocab(self, args: List[Any]) -> None:
        """
        Validate URIs in col against allowed vocabularies for that controlled vocab

        Args:
            args: [column_name] - the col header for validation
        """
        col: str = args[0]
        df = self.get_dataframe()
        
        controlled_vocab = self.validator_mapping.get(col.lower())
        logger.debug(f"controlled_vocab for '{col}': {controlled_vocab}")
        if not controlled_vocab:
            logger.error(f"No controlled vocab mapping for '{col}'")
            return
        
        logger.debug(f"validation_mappings keys: {list(self.validation_mappings.keys())}")
        logger.debug(f"controlled_vocab_map keys: {list(self.validation_mappings.get('controlled_vocab_map', {}).keys())}")
        
        try:
            vocab_list = self.validation_mappings['controlled_vocab_map'][controlled_vocab]
        except KeyError:
            logger.error(f"controlled_vocab_map missing entry for '{controlled_vocab}' in validation_mappings.yaml")
            return
        
        logger.debug(f"Validating '{col}' against vocabularies: {', '.join(vocab_list)}")
        # FIXME: don't use iterrows, it's inefficient because it loops through the whole df. Just do the header
        for index, row in df.iterrows():
            if pd.notna(row[col]):
                cell = row[col]
                for value in str(cell).split('|'):
                    value = value.strip()
                    if not value:
                        continue
                    valid = False
                    for vocab_name in vocab_list:
                        validator = vocabularies.VOCABULARY_VALIDATORS.get(vocab_name)
                        if validator and validator(value):
                            valid = True
                            logger.debug(f"  row {index + 2}: '{value}' matched {vocab_name}")
                            break
                    if not valid:
                        logger.error(f"row {index + 2}: '{value}' does not match any vocabulary in ({', '.join(vocab_list)})")