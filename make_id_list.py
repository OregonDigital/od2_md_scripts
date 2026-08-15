"""Generate pipe-separated list of files"""
import csv, os
from utils import is_complex

# Could make a function that does this outside of main, so that you can call that to automate this whole part of the process

def main():
    filepath = input("Enter filepath to csv\n>>> ")
    with open(filepath, "r", encoding="utf-8-sig") as csvf:
            reader = csv.DictReader(csvf)
            unformatted_ids = []

            for row in reader:
                # Should be "id" column from export by default, but possible to change this if needed
                row_id = (row.get("id", "")).strip()
                if not row_id:
                     raise ValueError(f"Blank id found at row {reader.line_num}")
                if not is_complex(row):
                     unformatted_ids.append(row_id)
            
    formatted_ids = '|'.join(unformatted_ids)
    print(formatted_ids)


if __name__ == "__main__":
    main()