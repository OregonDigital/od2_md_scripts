"""
Automated fixes for common CSV metadata issues.
Reads file path from filepaths.yaml and applies fixes from collection-specific config. 

Usage: python3 fixcsv.py <collection-name>
Example: python3 fixcsv.py uo-athletics
"""

import yaml
import pandas as pd
import logging
from pathlib import Path
import shutil
import sys
import re
from typing import Any, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def load_filepaths() -> list[str]:
    """Load metadata file path from filepaths.yaml"""
    with open("filepaths.yaml", "r") as yf:
        paths = yaml.safe_load(yf)
    return paths['metadata']


def load_dataframe(metadata_path: list[str]) -> pd.DataFrame:
    """Load CSV into DataFrame (assumes CSV format)"""
    if len(metadata_path) != 1:
        logger.error("For CSV, filepaths.yaml > metadata must be one-item list")
        sys.exit(1)
    
    filepath = metadata_path[0]
    if not filepath.endswith('.csv'):
        logger.error(f"Expected CSV file, got: {filepath}")
        sys.exit(1)
    
    return pd.read_csv(filepath, dtype=str)


def load_fix_config(collection_name: str) -> dict[str, Any]:
    """Load collection-specific fix config if it exists"""
    fix_config_path = f"config/{collection_name}-fixes.yaml"
    
    if not Path(fix_config_path).exists():
        logger.error(f"Fix config not found: {fix_config_path}")
        logger.error(f"Create {fix_config_path} with fix instructions")
        sys.exit(1)
    
    with open(fix_config_path, "r") as yf:
        config = yaml.safe_load(yf)
    
    if not config or 'fixes' not in config:
        logger.error(f"{fix_config_path} must contain 'fixes' list")
        sys.exit(1)
    
    return config


def load_validation_config(collection_name: str) -> dict[str, Any]:
    """Load the validation config to get expected values"""
    with open(f"config/{collection_name}.yaml", "r") as yf:
        return yaml.safe_load(yf)


def backup_original(filepath: str) -> str:
    """Create backup of original file"""
    backup_path = filepath + '.backup'
    shutil.copy(filepath, backup_path)
    logger.info(f"Backup created: {backup_path}")
    return backup_path


def fix_strip_column(df: pd.DataFrame, column: str) -> Tuple[pd.DataFrame, int]:
    """Strip leading/trailing whitespace from all values in a column"""
    if column not in df.columns:
        logger.warning(f"Column '{column}' not found in CSV, skipping")
        return df, 0
    
    changes = 0
    for idx in df.index:
        if pd.notna(df.at[idx, column]):
            original = str(df.at[idx, column])
            stripped = original.strip()
            if original != stripped:
                df.at[idx, column] = stripped
                changes += 1
                logger.debug(f"Row {idx+2}, '{column}': stripped whitespace")
    
    return df, changes


def fix_regex_replace(df: pd.DataFrame, column: str, pattern: str, replacement: str) -> Tuple[pd.DataFrame, int]:
    """Apply regex replacement to all values in a column"""
    if column not in df.columns:
        logger.warning(f"Column '{column}' not found in CSV, skipping")
        return df, 0
    
    changes = 0
    compiled_pattern = re.compile(pattern)
    
    # Apply the replacement to every value -- if it's different than the original, it must have been changed (and an error before)
    # If it's the same, then it was good before
    # This doesn't repeat things like .tif extensions because the fix yaml already specifies to exclude things ending in .tif.
    for idx in df.index:
        if pd.notna(df.at[idx, column]):
            original = str(df.at[idx, column])
            replaced = compiled_pattern.sub(replacement, original)
            if original != replaced:
                df.at[idx, column] = replaced
                changes += 1
                logger.debug(f"Row {idx+2}, '{column}': '{original}' -> '{replaced}'")
    
    return df, changes


def fix_enforce_string(df: pd.DataFrame, column: str, validation_config: dict[str, Any]) -> Tuple[pd.DataFrame, int]:
    """Enforce the string value defined in validation config"""
    # Look up what the string should be
    if column not in validation_config or not validation_config[column]:
        logger.warning(f"No validation rule for '{column}', skipping")
        return df, 0
    
    # Find the string validation rule
    expected_value = None
    for rule in validation_config[column]:
        if rule.get('string'):
            expected_value = rule['string']
            break
    
    if not expected_value:
        logger.warning(f"No string rule for '{column}', skipping")
        return df, 0
    
    # Apply the fix
    changes = 0
    for idx in df.index:
        if pd.notna(df.at[idx, column]):
            current = str(df.at[idx, column])
            if current != expected_value:
                df.at[idx, column] = expected_value
                changes += 1
    
    return df, changes


def apply_collection_fixes(df: pd.DataFrame, fix_config: dict[str, Any]) -> Tuple[pd.DataFrame, int]:
    """Apply collection-specific fixes from config"""
    total_changes = 0
    
    for fix in fix_config['fixes']:
        fix_type = fix.get('type')
        
        if fix_type == 'strip':
            column = fix.get('column')
            if not column:
                logger.error(f"Fix missing 'column' field: {fix}")
                continue
            
            df, changes = fix_strip_column(df, column)
            logger.info(f"  Strip whitespace in '{column}': {changes} changes")
            total_changes += changes
            
        elif fix_type == 'regex_replace':
            column = fix.get('column')
            pattern = fix.get('pattern')
            replacement = fix.get('replacement')
            
            if not all([column, pattern, replacement]):
                logger.error(f"regex_replace missing required fields: {fix}")
                continue
            
            df, changes = fix_regex_replace(df, column, pattern, replacement)
            logger.info(f"  Regex replace in '{column}': {changes} changes")
            total_changes += changes
            
        else:
            logger.error(f"Unknown fix type '{fix_type}': {fix}")
    
    return df, total_changes


def save_dataframe(df: pd.DataFrame, metadata_path: list[str]) -> None:
    """Save fixed DataFrame back to CSV"""
    filepath = metadata_path[0]
    df.to_csv(filepath, index=False)
    logger.info(f"Saved to: {filepath}")


def main() -> None:
    """Main execution"""
    logger.info("="*60)
    logger.info("CSV Auto-Fix Tool")
    logger.info("="*60)
    
    # Get collection name from command line
    if len(sys.argv) < 2:
        logger.error("Usage: python3 fixcsv.py <collection-name>")
        logger.error("Example: python3 fixcsv.py uo-athletics")
        sys.exit(1)
    
    collection = sys.argv[1]
    logger.info(f"Collection: {collection}")
    
    # Load fix configuration
    fix_config = load_fix_config(collection)
    logger.info(f"Loaded {len(fix_config['fixes'])} fix rules from config/{collection}-fixes.yaml")
    
    # Load file path
    metadata_path = load_filepaths()
    logger.info(f"Loading: {metadata_path[0]}")
    
    # Create backup
    backup_original(metadata_path[0])
    
    # Load data
    df = load_dataframe(metadata_path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Load validation config
    validation_config = load_validation_config(collection)
    logger.info(f"Loaded validation config for {collection}")
    
    # You might expect to see process.py run here or some method to determine what to fix. There isn't any, 
    # because every fix is running every time. For some, redundancy doesn't matter (like strip) and for others (regex_replace),
    # it's being checked against a pattern. That pattern should already exclude valid entries in the case of using regex_replace to append to the end,
    # and moves on when it detects them. (This is how it checks the number of values changed -- add up any
    # changed values that don't match the unchanged value). 

    # Apply fixes
    logger.info(f"\nApplying fixes...")
    df, total_changes = apply_collection_fixes(df, fix_config)
    
    # Enforce validation rules
    logger.info("\nEnforcing validation rules...")
    for column in validation_config.keys():
        df, changes = fix_enforce_string(df, column, validation_config)
        logger.info(f"  Enforce string in '{column}': {changes} changes")
        total_changes += changes
    
    # Save if changes were made
    if total_changes > 0:
        logger.info("")
        save_dataframe(df, metadata_path)
        logger.info(f"\n✓ Applied {total_changes} fixes")
        logger.info(f"Run 'python3 process.py {collection}' to validate")
    else:
        logger.info(f"\n✓ No issues found - file is clean")
    
    logger.info("="*60)


if __name__ == "__main__":
    main()
