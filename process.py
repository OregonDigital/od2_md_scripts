import sys
from od2ingest import Ingest

try:
    processing = Ingest(sys.argv[1])
    processing.process_columns()
    files_check = input("check metadata filenames against files/ assets? (y/n)\n>>>")
    if files_check.lower() == 'y':
        processing.check_filenames_assets()
except IndexError:
    print(f"(!) MISSING config file name (do not include file extension)")
    print("EXAMPLE command:")
    print("> python process.py uo-athletics")
