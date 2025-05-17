import sys
from od2ingest import Ingest

try:
    processing = Ingest(sys.argv[1])
    headers_match = processing.check_columns_config()
    if headers_match == True:
        processing.process_columns()
        # to do: eliminate following processing, process this from config file
        print("(*) UO Athletics")
        files_check = input("check (filename - extension) = identifier? (y/n)\n>>>")
        if files_check.lower() == 'y':
            processing.id_match_file()
except IndexError:
    print(f"(!) MISSING config file name (do not include file extension)")
    print("EXAMPLE command:")
    print("> python process.py uo-athletics")
