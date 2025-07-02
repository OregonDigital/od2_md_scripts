from od2validation import Package
import sys

try:
    processing = Package(sys.argv[1])
    # print(type(processing)) # check
    processing.print_filepaths()
    processing.check_headers()
    processing.get_headers_instructions()
except IndexError:
    print("(!!) command missing config file name (do not include file extension)")
    print("EXAMPLE:\n> python3 process.py uo-athletics")
