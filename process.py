import sys
from od2ingest import Ingest

if sys.argv[1]:
    processing = Ingest(sys.argv[1])
    processing.process_columns()
    files_check = input("check metadata filenames against files/ assets? (y/n)\n>>>")
    if files_check.lower() == 'y':
        processing.check_filenames_assets()
    else:
        pass
else:
    print("missing: config file name (minus file format extension)")
