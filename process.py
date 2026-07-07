from od2validation import Package, ValidationError
import sys
import logging
from typing import List, Optional

# Set up logging (level is set to INFO, format tells log how to display messages)
# format uses a weird syntax because logging uses older string format style
logging.basicConfig(
    level=logging.INFO,
    # Display the level of the log name (like INFO or DEBUG) and then the log message after whitespace
    format='%(levelname)s:     %(message)s'
)

# process.py is the entry point for the script, so we set the logging level for the whole program here
logger = logging.getLogger(__name__)

def count_header_errors(errors, headers) -> dict[str, int]:
    """Summarize error totals per header"""
    d = {}
    for h in headers:
        d[h] = 0
    for e in errors:
        if e.error_header in d:
            d[e.error_header] += 1
        else:
            print(f"Header {e.error_header} present in errors but not in header list")
    return d

def print_error_totals(error_totals: dict[str, int]) -> None:
    print("\nERROR TOTALS:\n")
    for header in error_totals:
        if error_totals[header] != 0:
            print(f"{header}: {error_totals[header]}")

def main():
    try:
        # Run checks and print errors
        collection_name = sys.argv[1]
        processing = Package(collection_name)
        processing.print_filepaths()
        processing.check_headers()
        errors = processing.get_headers_instructions()
        error_totals = count_header_errors(errors, processing.get_headers())
        print_error_totals(error_totals)

        # Derive error variables
        error_count = len(errors)
        headers_with_errors = set(e.error_header for e in errors)
        validated_headers = processing.get_headers()

        # Print summary
        print("\n" + "="*70)
        print("-- Validation complete --")
        print(f"Checked {len(validated_headers)} headers")
        if error_count == 0:
            print("NO ERRORS FOUND")
        else:
            print(f"Found {error_count} error(s) in {len(headers_with_errors)}/{len(validated_headers)} headers")
            print(f"Headers with errors: {', '.join(sorted(headers_with_errors))}")
            print("\nTo automatically fix common issues:")
            print(f"  python fixcsv.py {collection_name}")
            print("\nNote: this file is not created by default, you will have to make it manually")
        print("="*70)
        
    except IndexError:
        print("Missing config file name (do not include file extension)")
        print("EXAMPLE: python process.py uo-athletics")

if __name__ == "__main__":
    main()