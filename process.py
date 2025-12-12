from od2validation import Package
import sys
import logging

# Configure logging (replaces print statements throughout codebase, including
# in od2validation.py lines that are called from this script)
# For more detailed debug information, change logging.INFO to logging.DEBUG
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

try:
    processing = Package(sys.argv[1])
    # print(type(processing)) # check
    processing.print_filepaths()
    processing.check_headers()
    processing.get_headers_instructions()
except IndexError:
    print("(!!) command missing config file name (do not include file extension)")
    print("EXAMPLE:\n> python3 process.py uo-athletics")
