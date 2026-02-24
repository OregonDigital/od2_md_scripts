# od2_md_scripts
Scripts for metadata validation prior to ingest in Oregon Digital, and verifying status of works that have been ingested. 

Now featuring [a wiki](https://github.com/OregonDigital/od2_md_scripts/wiki) which contains other guides and explanations.

# Setup
If you've used github before and are familiar with general programming, clone the repo and then follow the instructions in [Getting Started](https://github.com/OregonDigital/od2_md_scripts/wiki/Getting-Started). Otherwise, start with the guide below. 

## Downloading the Code
We're going to *clone the repo*, which means adding the code here to your computer files.
1. Click the green button near the top of this page that says "Code" and then copy the HTTP link to clipboard.
2. In your terminal on your computer navigate to the folder you want to add the program to, and then type "git clone (repository link)", replacing (repository link) with the one you just copied.

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

⚠️IN PROGRESS ⚠️

# Using the Program



## How do I run the code?

