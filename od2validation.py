"""Define Package class for data reading and parsing and Instructions classes to run validation checks"""
import yaml, os, json, re
import pandas as pd
import logging
from typing import Tuple, List, Dict, Any, Optional, Pattern
import vocabularies, utils
import copy
from abc import ABC, abstractmethod

# Logger replaces print statements for debugging/usage
# (It basically controls the level of info to print)
logger = logging.getLogger(__name__)

class Package(object):

    def __init__(self, headers_config: str) -> None:
        self.metadata = self.filepaths()[0]
        self.assets = os.listdir(self.filepaths()[1])
        # Running get_config on the yaml file (name passed in through process.py creating Package()) the user specified in the command line
        self.default_config, self.headers_config, self.validation_mappings = self.get_config(headers_config)
        # Build validator map - links auto-validated fields to their common validator (ex. 'photographer' -> 'creator')
        self.validator_mapping = self._build_validator_mapping()

    def filepaths(self) -> Tuple[List[str], str]:
        with open("filepaths.yaml", "r") as yf:
            paths: Dict[str, Any] = yaml.safe_load(yf)
            return (paths['metadata'], paths['assets'],)
            # * self.metadata is 1 or 2 item list

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
        with open("headers_fixes_config/default.yaml", "r") as yf:
            default: Dict[str, Any] = yaml.safe_load(yf)
        with open(f"headers_fixes_config/{headers_config}.yaml", "r") as yf:
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
        """Check that all headers in the yaml config exist in metadata (where a base header in yaml like subject covers all enumerated headers like subject_1, subject_2, ...)"""
        check: bool = True
        logger.info("check headers configuration / headers in metadata")

        # Compare base headers to config, not the actual csv headers. Otherwise headers_config won't match, 
        # since it has only base headers while csv could have enumerated headers

        # Get actual existing csv headers (so enumerated headers are possible)
        real_headers = self.get_headers()
        # Get all base headers (duplicates are possible for sliced enumerated headers, but no enumeration is possible)
        base_headers = [utils.base_header(h) for h in real_headers]
        # Remove duplicate headers (no duplicates or enumerated headers now)
        real_base_headers = set(base_headers)


        if set(self.headers_config) != set(real_base_headers):
            check = False
            logger.error("headers_config != metadata headers")
            diff: List[str] = list(real_base_headers - set(self.headers_config))
            if len(diff) > 0:
                logger.info("metadata headers not in config file:")
                for item in diff:
                    logger.error("  %s", item)
            diff: List[str] = list(set(self.headers_config) - real_base_headers)
            if len(diff) > 0:
                logger.error("headers_config fields not in metadata headers:")
                for item in diff:
                    logger.error("  %s", item)
            logger.error("update metadata headers and/or headers_config and retry")
        else:
            pass
        return check


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
            if instruction.get('validate_controlled_vocab'):
                # Replace old name with new name in args
                instruction['validate_controlled_vocab'] = [new_name if arg == old_name else arg for arg in instruction['validate_controlled_vocab']]
        return updated_instructions

    def get_headers_instructions(self) -> List[Optional[ValidationError]]:
        """
        Run the whole instruction loop: check each header, apply checks to rows under the header
        """
        df = self.get_dataframe()
        errors = []
        # Loop through each header, running instructions for each
        for real_header in self.get_headers():
            # Loop through resolved (either from specific config or default) instructions
            # Generally there's only 1, but possible to have more like in file in uo-athletics
            for instruction in self._resolve_instructions(real_header):
                errors.extend(self._run_instruction(df, real_header, instruction))
        return errors
    
    def _select_rows(self, df: pd.DataFrame, which: str) -> pd.DataFrame:
        """Return filtered df that filters for all, only complex objects, or only items"""
        if which == "all":
            return df
        if which == "complex":
            if "format" not in df.columns:
                logger.error("complex objects need 'format' col")
                return df.iloc[0:0]
            return df[df["format"] == "https://w3id.org/spar/mediatype/application/xml"]
        if which == "item":
            if "format" not in df.columns:
                logger.error("complex object has unexpected 'format' value")
                return df.iloc[0:0]
            return df[(df["format"].isna()) | (df["format"] != "https://w3id.org/spar/mediatype/application/xml")]
        logger.error(f"Invalid 'which' parameter: {which}")
        return df.iloc[0:0]
    
    def _resolve_instructions(self, real_header: str):
        """Return instructions (config) for a header, with updated header names if using auto validator"""
        
        header = utils.base_header(real_header)
        config = self.headers_config.get(header)
        # Use the project-specific config
        if config is not None:
            logger.info(f"Validating '{real_header}' from config...")
            return config
        
        # Use a mapped validator if one exists (ex. 'collector', 'author', or 'illustrator' could be mapped to Creator and use Creator validation)
        validator_type = self.validator_mapping.get(header.lower())
        if validator_type and validator_type in self.default_config:
            logger.info(f"Validating '{real_header}' from default config (mapped to '{validator_type}')")
            # Default validation has default yaml fields, so we have to replace them or they don't match the csv
            # Ex. 'collector' gets replaced by 'creator' unless we update the args
            return self._update_method_args(self.default_config[validator_type], validator_type, header)
    
        # Use the default validation (headers_fixes_config/default.yaml) config
        fallback = self.default_config.get(header)
        if fallback is not None:
            logger.info(f"Validating '{real_header}' from default config...")
            return fallback
        
        logger.info(f"NO VALIDATION CHECK CONFIGURED FOR '{real_header}' in headers_config or default")
        return []

    def _run_instruction(self, df: pd.DataFrame, header: str, instruction: Dict) -> List[Optional[ValidationError]]:
        """Instantiate Instruction subclass and execute it on given header, selecting rows by 'which' in instruction)"""
        # Get 'which' from the instruction, then select rows based on it (default to "all" if no value found)
        which = instruction.get("which", "all")
        rows = self._select_rows(df, which)
        # Create an instruction subclass (String, Regex, FilenamesAssets, etc.) and execute it
        errors = Instruction.from_dict(instruction).execute(self, df, header, rows)
        return errors

    def _combine_enumerated_headers(self, header: str, df: pd.DataFrame) -> List[str]:
        """
        Return all cols that belong to one header type
        Ex. subject_1, subject_2, subject_3
        """
        pattern = re.compile(rf"^{re.escape(header)}(?:_\d+)?$")
        return [col for col in df.columns if pattern.match(col)]
    
    def _flatten_cell_values(self, value: Any) -> List[str]:
        """
        Normalize one cell into a flat list of values. Splits pipe-delimited cells and removes empty cells
        """
        if pd.isna(value):
            return []
        return [part for part in str(value).split("|") if part]

    def values_for_header(self, df: pd.DataFrame, header: str, row_idx: int) -> List[str]:
        """
        Collect all values for one header from matching cols in a given row
        """
        values: List[str] = []
        for col in self._combine_enumerated_headers(header, df):
            # Appends all values from flatten_cell_values as individual items in list
            values.extend(self._flatten_cell_values(df.at[row_idx, col]))
        return values

class Instruction(ABC):
    row_scoped = True #FIXME find better name

    @abstractmethod
    def execute(self, package, df, header, rows) -> List[Optional[ValidationError]]:
        """Run an instruction, where package is the Package instance"""
        raise NotImplementedError

    @staticmethod
    def from_dict(d: dict) -> Instruction:
        """Instantiate an Instruction subclass (string, regex, etc.) based on the instructions dict"""
        if "string" in d:
            return StringInstruction(d["string"])
        if "regex" in d:
            return RegexInstruction(re.compile(str(d["regex"])))
        if "check_filenames_assets" in d:
            return FilenamesAssetsInstruction(d["check_filenames_assets"])
        if "identifier_file_match" in d:
            return IdentifierFileInstruction(d["identifier_file_match"])
        if "validate_controlled_vocab" in d:
            return ValidateControlledVocabInstruction(d["validate_controlled_vocab"])
        raise ValueError(f"Unknown instruction type: {d}")

class StringInstruction(Instruction):
    """Validate string values in a column against expected string value for the header"""
    def __init__(self, expected: str):
        self.expected = expected

    def execute(self, package, df, header, rows) -> List[Optional[ValidationError]]:
        validation_errors = []
        for idx in rows.index:
            # Check all values that are part of the header, whether enumerated or pipe separated
            for value in package.values_for_header(rows, header, idx):
                if self.expected != value:
                    error = ValidationError(idx+2, header, value, self.expected, f"row {idx + 2}: '{value}' != string '{self.expected}")
                    validation_errors.append(error)
                    logger.error(f"row {idx + 2}: '{value}' != string '{self.expected}")
        return validation_errors

class RegexInstruction(Instruction):
    """Validate string values in a column against expected regex pattern for the header"""
    def __init__(self, expected_pattern: Pattern[str]):
        self.expected_pattern = expected_pattern
    
    def execute(self, package, df, header, rows):
        validation_errors = []
        for idx in rows.index:
            # Check all values that are part of the header, whether enumerated or pipe separated
            for value in package.values_for_header(rows, header, idx):
                if not re.match(self.expected_pattern, value):
                    error = ValidationError(idx+2, header, value, self.expected_pattern, f"row {idx + 2}: '{value}' does not match regex for header values")
                    validation_errors.append(error)
                    logger.error(f"row {idx + 2}: '{value}' does not match regex for header values")
        return validation_errors
    
class FilenamesAssetsInstruction(Instruction):
    """
    Validate that all filenames in the csv match the actual asset file names in the assets folder
    """

    def __init__(self, args: List[Any]):
        self.args = args
    
    def execute(self, package, df, header, rows) -> List[Optional[ValidationError]]:
        col: str = self.args[0]
        base_col = utils.base_header(col)
        validation_errors: List[ValidationError] = []

        # Building dict mapping file names to the row where each filename appears 
        # (this assumes file names are unique per sheet)
        filenames_by_value: Dict[str, int] = {}
        for idx in df.index:
            for v in package.values_for_header(df, base_col, idx):
                #FIXME Skip empty? That's what we do now with the strip and 'if not v'
                v = v.strip()
                if not v:
                    continue
                # Map filename to row
                filenames_by_value[v] = idx + 2
        
        # Make filenames and assets into sets for easy comparison
        filenames_set = set(filenames_by_value.keys())
        assets_set = set(package.assets)

        # Compare each set (get what's missng from each)
        extra_filenames = filenames_set - assets_set
        missing_assets = assets_set - filenames_set

        # List all extra files and extra assets
        for file in sorted(extra_filenames):
            row = filenames_by_value.get(file)
            validation_errors.append(ValidationError(row, col, file, None, f"'{file}' not in assets/"))
            logger.error(f"row {row}: '{file}' not in assets/")
        
        for asset in sorted(missing_assets):
            validation_errors.append(ValidationError(None, col, asset, None, f"'{asset}' exists in assets but not in csv"))
            logger.error(f"row {row}: '{asset}' exists in assets but not in csv")
            
        return validation_errors

class IdentifierFileInstruction(Instruction):
    """
    Check that identifier values match filename values without the file ending (compare identifier col to file col). 
    Only works for one of each, can't be enumerated or pipe separated.
    """
    def __init__(self, args: List[Any]):
        self.args = args
    
    def execute(self, package, df, header, rows) -> None:
        substring: str = self.args[0]
        df_for_method: pd.DataFrame = package.get_dataframe()
        validation_errors = []
        
        for index, row in df_for_method.iterrows():
            actual_id = str(row['identifier'])
            # Remove file ending from file (leftover should match identifier)
            expected_id = str(row['file']).replace(substring, '')
            if actual_id == expected_id:
                continue
            else:
                validation_errors.append(ValidationError(row, 'identifier', actual_id, expected_id, f"{row['identifier']} doesn't match '{row['file']}'"))
                logger.error(f"row {index + 2}: '{row['identifier']} doesn't match '{row['file']}'")

        return validation_errors
    
class ValidateControlledVocabInstruction(Instruction):
    """
    Validate URIs in col against allowed vocabularies for that controlled vocab
    """
    def __init__(self, args: List[Any]):
        self.args = args

    def execute(self, package, df, header, rows) -> None:
        col: str = self.args[0]
        df = package.get_dataframe()
        validation_errors = []
        
        # Get controlled vocab type
        controlled_vocab = package.validator_mapping.get(col.lower())
        logger.debug(f"controlled_vocab for '{col}': {controlled_vocab}")
        if not controlled_vocab:
            logger.error(f"No controlled vocab mapping for '{col}'")
            return
        
        logger.debug(f"validation_mappings keys: {list(package.validation_mappings.keys())}")
        logger.debug(f"controlled_vocab_map keys: {list(package.validation_mappings.get('controlled_vocab_map', {}).keys())}")
        
        # Get possible vocabularies from a controlled vocab
        try:
            vocab_list = package.validation_mappings['controlled_vocab_map'][controlled_vocab]
            # ex. 'lcnaf' or 'ulan'
        except KeyError:
            logger.error(f"controlled_vocab_map missing entry for '{controlled_vocab}' in validation_mappings.yaml")
            return
        
        logger.debug(f"Validating '{col}' against vocabularies: {', '.join(vocab_list)}")

        for idx in rows.index:
            # Check all values for header, including enumerated and pipe separated. Empty cells already skipped in values_for_header
            for value in package.values_for_header(rows, header, idx):
                if not value:
                    continue
                valid = False
                # Try all validators, if any pass then it's correctly formatted
                for vocab_name in vocab_list:
                    validator = vocabularies.VOCABULARY_VALIDATORS.get(vocab_name)
                    if validator and validator(value):
                        valid = True
                        logger.debug(f"  row {idx + 2}: '{value}' matched {vocab_name}")
                        break
                if not valid:
                    validation_errors.append(ValidationError(idx+2, header, value, None, f"'{value}' does not match any vocabulary in ({', '.join(vocab_list)})"))
                    logger.error(f"row {idx + 2}: '{value}' does not match any vocabulary in ({', '.join(vocab_list)})")

        return validation_errors

class ValidationError:
    """Contains error attributes for easy access and counting"""
    def __init__(self, error_row: int, error_header, value, expected_value, error_message):
        # Pass the actual error row as would be seen in the csv, not the df row (likely add 2 to idx)
        self.error_row = error_row
        self.error_header = error_header
        self.value = value
        self.expected_value = expected_value
        self.error_message = error_message
        # self.validation_status = (could be bool where true = validated and false = error with validation, or maybe more specific?)

    # Define comparison method for <, which is used in sorting
    def __lt__(self, other: ValidationError):
        return self.error_row < other.error_row
    
    # Define how to print a validation error (this is what's displayed in print(error) where error is type ValidationError)
    def __str__(self):
        return self.error_message
    