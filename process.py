import sys
from od2ingest import Ingest

headers = True

try:
    processing = Ingest(sys.argv[1])
    headers = processing.check_columns_config()
    if headers == True:
        processing.process_columns()
        print("(*) UO Athletics")
        files_check = input("check (filename - extension) = identifier? (y/n)\n>>>")
        if files_check.lower() == 'y':
            processing.id_match_file()
except IndexError:
    print(f"(!) MISSING config file name (do not include file extension)")
    print("EXAMPLE command:")
    print("> python process.py uo-athletics")
