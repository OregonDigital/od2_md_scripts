"""Generate pipe-separated list of files"""
import csv, os

# Could make a function that does this outside of main, so that you can call that to automate this whole part of the process

def main():
    filepath = input("Enter filepath to csv: ")
    with open(filepath, "r", encoding="utf-8-sig") as csvf:
            reader = csv.DictReader(csvf)
            #FIXME: This won't ignore if a complex ID is in the column
            unformatted_ids = [row["identifier"] for row in reader]
    formatted_ids = '|'.join(unformatted_ids)
    print(formatted_ids)


if __name__ == "__main__":
    main()