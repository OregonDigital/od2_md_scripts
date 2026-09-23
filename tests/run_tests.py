import sys
import os

# Need this line to let us import od2validation, since it's an extra folder up in the code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from od2validation import Package

"""FIXME:
- It's nicer to keep test header configs in the tests folder, but get_headers_instructions uses get_config,
  which explicitly grabs config from headers_fixes_config folder. So we might have to keep them in headers_fixes_config
- Alternatively, we could just use uo-athletics.yaml to check. But the problem is then we are testing not just whether
  our check functions work, but also whether our actual yaml is set up correctly at the same time. Becomes harder to find
  which is the problem.
"""
def check_correct_athletics():
    print("Runninng check_correct_athletics...")
    # Expect 0 errors, so empty list
    expected_errors = []
    filepaths = "tests/test_filepaths/check_correct_athletics.yaml"

    # Collection name determines the yaml to use (it's )
    collection_name = "uo-athletics"
    # Point to filepaths.yaml for this check
    processing = Package(collection_name, filepaths_yaml=filepaths)
    processing.print_filepaths()
    processing.check_headers()
    errors = processing.get_headers_instructions()
    assert errors == expected_errors, f"Got errors {errors} where None were expected"

def check_missing_fields():
    print("Running check_missing_fields...")
    # Manually enter the exact errors we expect for a missing value in each field
    expected_errors = []
    filepaths=""

    collection_name = "uo-athletics"
    processing = Package(collection_name, filepaths_yaml=filepaths)
    processing.print_filepaths()
    processing.check_headers()
    errors = processing.get_headers_instructions()
    assert errors == expected_errors, f"Unexpected or missing errors: {errors} vs. {expected_errors}"

def check_bad_values():
    print("Running check_bad_values...")
    # Manually enter the exact errors we expect for a bad value in each field
    expected_errors = []
    
    collection_name = "uo-athletics"
    processing = Package(collection_name)
    processing.print_filepaths()
    processing.check_headers()
    errors = processing.get_headers_instructions()
    assert errors == expected_errors, f"Unexpected or missing errors: {errors} vs. {expected_errors}"

def main():
    print("-- RUNNING TESTS FOR VALIDATION --\n")
    check_correct_athletics()
    # check_missing_fields()
    # check_bad_values()
    print("-- TESTING COMPLETE --")

if __name__ == "__main__":
    main()