"""Generate pipe-separated list of files"""
import csv, os

# Could make a function that does this outside of main, so that you can call that to automate this whole part of the process

#FIXME: Currently includes complex object id in the list. Skip this using is_complex from utils
def main():
    filepath = input("Enter filepath to csv: ")
    with open(filepath, "r", encoding="utf-8-sig") as csvf:
            reader = csv.DictReader(csvf)
            # Should be "id" column from export by default, but possible to change this if needed
            unformatted_ids = [row["id"] for row in reader]
    formatted_ids = '|'.join(unformatted_ids)
    print(formatted_ids)


if __name__ == "__main__":
    main()