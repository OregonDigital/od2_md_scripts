# od2_md_scripts
Scripts for metadata validation prior to ingest in Oregon Digital, and verifying status of works that have been ingested. 

Now featuring [a wiki](https://github.com/OregonDigital/od2_md_scripts/wiki) which contains other guides and explanations.

# Setup
If you've used github before and are familiar with general programming, clone the repo and then follow the instructions in [Getting Started](https://github.com/OregonDigital/od2_md_scripts/wiki/Getting-Started). Otherwise, start with the guide below. 

## Downloading the Code
We're going to *clone the repo*, which means adding the code here to your computer files.
1. Click the green button near the top of this page that says "Code" and then copy the HTTP link to clipboard.
2. In the terminal on your computer navigate to the folder you want to add the program to, and then type "git clone (repository link)", replacing (repository link) with the one you just copied.

Now you have the code locally saved to your computer! It lives in the file you were in in terminal when you ran git clone.

For more information about cloning the repo, check out the [docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Making Your Files
There are a few files that you will need to manually edit in order for the code to run. You can do this with your terminal, in any text editor you like, or an IDE like VSCode -- whatever you feel most comfortable with. 

### Making filepaths.yaml
1. Copy filepaths_example.yaml (it's at the top level of the code folder, keep it there when you copy).
2. Rename the copy to 'filepaths.yaml'.
3. Replace the line under metadata with the file path to your csv.

WARNING: Do not delete the "- " before your file path under metadata, it is part of the YAML format and will break without that.

4. Replace the assets line with the link to your folder of assets. It must be titled 'files'.

This is the process you'll use every time you want to select which csv and files to validate, since this tells the program the location of the files to check.

## Making Your Headers Config File
Your headers config file tells the program what you expect your metadata values to look like. It includes which headers you expect, what the acceptable values for cells are, even if any of them should always be the same value (for example, maybe your collection only ever has 1 photographer, so you know the value for the photographer column should always be the same name).

1. In your terminal, type and enter
```bash
python makeconfig.py
```
If you get an error saying you don't have Python installed, you either need to [check your version](https://www.howtogeek.com/796841/check-python-version/) or [install Python](https://www.python.org/downloads/)

2. Follow the instructions in the terminal

WARNING: DO NOT use spaces in the name of your config file, it will be very annoying for you to use later and could break the code.

⚠️IN PROGRESS ⚠️

## Making a Fix File
TODO

# Using the Program

## Validating Metadata Pre-Upload
Before you import files with metadata to OD2, this script lets you automatically validate your metadata. Validation requires a file to check values against, which is what we just made in Setup under Making Your Headers Config File. Default validation is a work-in-progress, but as of 2/24/2026 it automatically validates that any Creator-like URI like photographer, author, or artist is correctly formatted.

1. Before validating, make sure you have the file you want to validate set as the path in filepaths.yaml (you need to set both the csv path and the files path -- described above in 'Making filepaths.yaml'
2. To do the validation, you just need to run this command in your terminal:
```bash
python process.py [config file name]
```
Do not include the .yaml on the end of the config file.

This will show you a list of headers with errors in your spreadsheet.
