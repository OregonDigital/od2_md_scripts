# ⚠️IN PROGRESS ⚠️
# od2_md_scripts
Scripts for metadata validation prior to ingest in Oregon Digital, and verifying status of works that have been ingested. 

Now featuring [a wiki](https://github.com/OregonDigital/od2_md_scripts/wiki) which contains other guides and explanations.

# Setup

The Setup section walks you through how to make the files you'll need, with links to expand on them if you'd like to.

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
Your headers config file tells the program what you expect your metadata values to look like. At its most basic it includes only the headers from your metadata followed by a null tilda ~. The basic version will automatically check that the files in the metadata under the 'file' header match the files in your assets folder (called 'files'), and that your creator field has a valid URI format. You can add more yaml and some regex to include what the acceptable values for cells are (either one single value or a range of possible ones). 

**1. In your terminal, type and enter**
```bash
python makeconfig.py
```
If you get an error saying you don't have Python installed, you either need to [check your version](https://www.howtogeek.com/796841/check-python-version/) or [install Python](https://www.python.org/downloads/).

**2. Follow the instructions in the terminal**

WARNING: DO NOT use spaces in the name of your config file, it will break the code.

**3. Make the checks for each header (optional)**

This step is optional, as it adds a lot of utility but also requires some regex and yaml knowledge, or the willingness to learn. Custom checks allow you to specify exactly what values or range of values you expect for a field, so you can detect if there's bad data without manually reading every column. To learn how to make your own checks for headers, read [Custom Checks in Headers Config](https://github.com/OregonDigital/od2_md_scripts/wiki/Custom-Checks-in-Headers-Config).

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

Ex:
```bash
python process.py uo-athletics
```

This will show you a list of headers with errors in your spreadsheet. You can manually fix them and then run the check again, or if you've set up auto fixes you could run those and then check.
Remember that to validate another work, you just have to replace the filepaths in filepath.yaml like we did when we set up the file.

## Auto-Fixing Works
You'll see a prompt after running process.py if there are errors saying you can run autofix. If you've set it up, you just enter:
```bash
python fixcsv.py [collection-name]
```
This is all there is to it, and you'll get a list of errors that were fixed. If you get an error, make sure you're typing the collection name, not the collection name with '-fixes' at the end. Also make sure your fixes file is exactly named "[collection name]-fixes". You can re-run process.py to check if everything was fixed now.

## Checking Status of Uploaded Works
You can see a variety of features about works you've uploaded with the importer-solr.py module. This will let you check if there are any glitches with importing that need to be resolved, and give a high-level overview of the works before you manually review them.

To run the check, just type this into the terminal:
```bash
python importer-solr.py [importer id] [number of works within the collection]
```
Ex:
```bash
python importer-solr.py 4359 44
```
For a list of what each field that importer-solr returns means, read [Importer Solr Check Fields](https://github.com/OregonDigital/od2_md_scripts/wiki/Importer-Solr-Check-Fields).
