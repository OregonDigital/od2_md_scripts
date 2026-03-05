# ⚠️IN PROGRESS ⚠️
# od2_md_scripts
Scripts for metadata validation prior to ingest in Oregon Digital, and verifying status of works that have been ingested. 

Now featuring [a wiki](https://github.com/OregonDigital/od2_md_scripts/wiki) which contains other guides and explanations.

# Setup
If you've used github before and are familiar with general programming, clone the repo and then follow the instructions in [Getting Started](https://github.com/OregonDigital/od2_md_scripts/wiki/Getting-Started). Otherwise, start with the guide below. 

## Downloading the Code

Clone the repo to your device first. If you don't know how, check out the [docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Making Your Files
There are a few files that you will need to manually edit in order for the code to run. You can do this with your terminal, in any text editor you like, or an IDE like VSCode -- whatever you feel most comfortable with. 

### Making filepaths.yaml
1. Copy [filepaths_example.yaml](filepaths_example.yaml) (it's at the top level of the code folder, keep it there when you copy).
2. Rename the copy to 'filepaths.yaml'.
3. Replace the line under metadata with the file path to your csv.

WARNING: Do not delete the "- " before your file path under metadata, it is part of the YAML format and will break without that.

4. Replace the assets line with the link to your folder of assets. It must be titled 'files'.

This is the process you'll use every time you want to select which csv and files to validate, since this tells the program the location of the files to check.

### Making Your Headers Config File
Your headers config file tells the program what you expect your metadata values to look like. It includes which headers you expect, what the acceptable values for cells are, even if any of them should always be the same value (for example, maybe your collection only ever has 1 photographer, so you know the value for the photographer column should always be the same name).

1. In your terminal, type and enter
```bash
python makeconfig.py
```
If you get an error saying you don't have Python installed, you either need to [check your version](https://www.howtogeek.com/796841/check-python-version/) or [install Python](https://www.python.org/downloads/)

2. Follow the instructions in the terminal

WARNING: DO NOT use spaces in the name of your config file, it will break the code.

3. Make the checks for each header

There's 2 ways to check values under a header, and there's 2 special methods you may want to use. 

*Checking values under a header:* 

1. string

A string check just lets you specify exactly what a value should be for every cell in a column (under a header). For example, if I know that the license for a particular collection will always be "http://creativecommons.org/licenses/by-nc-nd/4.0/", then I can write a check to make sure it's that. 

Under the license header, I would write this:
```yaml
license:
  - string: http://creativecommons.org/licenses/by-nc-nd/4.0/
    which: all
```
The license is referring to the header I'm checking values for, the string shows what it should be, and the which specifies which values to apply it to (you can assume this will always be all).

2. regex

A regex check lets you check that values for a field that can change have an acceptable format. For example, the identifier might always start with "PH395_UP" followed by some characters. We can do a regex check to make sure the values fit that, even without knowing the specific values in a given identifier. It follows the same format, looking like:
```yaml
identifier:
  - regex: ^PH395_UP\S*$
    which: all
```
In this case, '\S*' is a regex part indicating there can be any number of non-whitespace characters at the end.

To check what your regex is doing, you could test it on [regex101](https://regex101.com/). For a tutorial, you could check [regexone](https://www.regexone.com/)

*Special methods:*

1. check_filenames_assets

Checking filenames and assets ensures that the filenames you have in your spreadsheet actually match the file names in the assets folder.

3. identifier_file_match

Checking the identifier and file for matches TODO

### Making a Fix File (Optional)

Fix files are optional because they can be complicated to correctly set up, at worst will *introduce* errors, and aren't necessary when you can manually fix sheets. However, fix files are very powerful tools when set up correctly because they can fix potentially hundreds of errors at once. It's up to you if you want to experiment with this. You must know or be willing to learn basic Regex and YAML to do this correctly.

Check the [Creating a Fix File](https://github.com/OregonDigital/od2_md_scripts/wiki/Creating-A-Fix-File) wiki page for the instructions on how to set it up.

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
