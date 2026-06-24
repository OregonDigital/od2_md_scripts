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
    """TODO"""
    d = {}
    for h in headers:
        d[h] = 0
    for e in errors:
        if e.error_header in d:
            d[e.error_header] += 1
        else:
            print(f"Header {e.error_header} present in errors but not in header list")
    return d

def print_errors(errors: List[Optional[ValidationError]]) -> None:
    """TODO"""
    headers_with_errors = set([h.error_header for h in errors])
    error_count = len(errors)
    errors_per_header = count_header_errors(errors, headers_with_errors)
    
    # List of errors under each header
    if headers_with_errors:
        for h in headers_with_errors:
            print(h + '\n')
            errors_under_h = sorted([e for e in errors if e.error_header == h])
            for e in errors_under_h:
                print(f"     {e}")

def main():
    try:
        # Run checks and print errors
        collection_name = sys.argv[1]
        processing = Package(collection_name)
        processing.print_filepaths()
        processing.check_headers()
        errors = processing.get_headers_instructions()
        print_errors(errors)

        # Derive error variables
        error_count = len(errors)
        headers_with_errors = set(e.error_header for e in errors)
        validated_headers = processing.get_headers()

        # Print summary
        print("\n" + "="*60)
        print("-- Validation complete --")
        print(f"Checked {len(validated_headers)} headers")
        if error_count == 0:
            print("NO ERRORS FOUND")
        else:
            print(f"Found {error_count} error(s) in {len(headers_with_errors)}/{len(validated_headers)} headers")
            print(f"Headers with errors: {', '.join(sorted(headers_with_errors))}")
            print("\nTo automatically fix common issues:")
            print(f"  python fixcsv.py {collection_name}")
            print("Note: this file is not created by default, you will have to make it manually")
        print("="*60)
        
    except IndexError:
        print("Missing config file name (do not include file extension)")
        print("EXAMPLE: python process.py uo-athletics")

if __name__ == "__main__":
    main()