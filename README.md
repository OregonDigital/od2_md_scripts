# ⚠️IN PROGRESS ⚠️
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

### Making Your Headers Config File
Your headers config file tells the program what you expect your metadata values to look like. It includes which headers you expect, what the acceptable values for cells are, even if any of them should always be the same value (for example, maybe your collection only ever has 1 photographer, so you know the value for the photographer column should always be the same name).

1. In your terminal, type and enter
```bash
python makeconfig.py
```
If you get an error saying you don't have Python installed, you either need to [check your version](https://www.howtogeek.com/796841/check-python-version/) or [install Python](https://www.python.org/downloads/)

2. Follow the instructions in the terminal

WARNING: DO NOT use spaces in the name of your config file, it will be very annoying for you to use later and could break the code.

TODO: need to offer detailed instructions on the Regex to actually select values once the config file is made

### Making a Fix File (Optional)

Note: fix files are optional because they can be complicated to correctly set up, at worst will *introduce* errors, and aren't necessary when you can manually fix sheets. However, fix files are very powerful tools when set up correctly because they can fix potentially hundreds of errors at once. It's up to you if you want to experiment with this. You must know or be willing to learn basic Regex and YAML to do this correctly.

A fix file, just like your headers config file, is specific to a collection. You can write specific fixes using pre-defined methods (which just require the name of the method and a little Regex) to do things like replace all values under a header with a single correct value or replace 'http://...' with 'https://...' in a URI. It will automatically make a backup of the file, just in case your fixes cause some issue. 

To actually set it up,
1. Create a file named "[headers config]-fixes.yaml" under od2_md_scripts/config. This file MUST be named exactly the same thing as your headers config file, with '-fixes' added before the .yaml extension, or the program won't detect it to use. 
2. Add yaml fields with each fix you want

Step 2 is actually somewhat complicated, so start with this template (you might want to copy and paste this into your fixes file):
```yaml
# hashtags followed by grey text are comments in yaml, these are just meant to be informative. They don't change the program
fixes:
  # this is the format for one simple fix
  - type: [method to use]
    column: [which header to replace values under]


  # this is the format for another fix, which could require more information if it's a different method
  - type: [another method (could be same or different)]
    column: [another header (could be same or different)]
    pattern: [only used with the regex_replace method, choosing what values to replace]
    replacement: [only used with the regex_replace method, choosing what value to use as replacement]

  ...
```

There are **3 methods** (chosen by 'type: ' in the yaml) you can use to do auto-fixes. 

Quick summary:
- 'strip': remove leading and trailing whitespace
- 'enforce_string': replace every value with a given string
- 'regex_replace': select a pattern (part of or a whole value in a cell) and replace it with another pattern


**Method 1: strip**

This will strip leading and trailing whitespace from all values in the column. All you need to do is enter the type and column as shown above, and it will be applied to every value under the header. 

Example: in the uo athletics collection, the 'institution' column often has an extra space after the each value. Usually it looks like this "http://id.loc.gov/authorities/names/n80126183 " instead of "http://id.loc.gov/authorities/names/n80126183". So the fix for that would be:

```yaml
fixes:
  # fix institution having extra space at the end
  - type: strip
    column: institution
```

**Method 2: enforce_string**

This will replace every value under a header with the same string. You just enter the type and column, as we did with Method 1, and the correct value will be retrieved from your headers config automatically. This can be confusing at first, so think of it this way: enforce_string is used when you know *exactly* what value you want for a field and it never changes. You would already be checking for that exact value in your headers config, so we just take that value and set all the cells to have it. This is why you don't actually write the value you want in the fixes file: it's already written in your headers config!

Example: in the uo athletics collection, the 'license' column was often set to the wrong type, an nc instead of nc-nd license. It would look like "http://creativecommons.org/licenses/by-nc/4.0/" when it should be "http://creativecommons.org/licenses/by-nc-nd/4.0/". And even if the column was left blank this would fix it, since we are just setting the value we want automatically. Here's how that fix looks like in the yaml file, including Method 1 so you can see multiple fixes together:
```yaml
fixes:
  # fix institution having extra space at the end
  - type: strip
    column: institution
  # fix license being wrong type
  - type: enforce_string
    column: license
```
Again, note that even though enforce_string is replacing cells with a specific value, we don't write that value here because it's already in the headers config.

**Method 3: regex_replace**

Regex_replace is the most powerful method, and the hardest to use. Regex_replace can append values to the end of a cell, insert a letter in the middle, and basically anything else you can think of. It has 4 fields in the yaml, unlike the 2 that strip and enforce_string have.

'type' and 'column' are the same as before. 

'pattern': this tells the program what to select 

'replacement': this tells the program what to replace selected values with

We'll give two examples here to show the variety of uses you might have for regex_replace. 

First, in uo-athletics the 'location' field requires a URI from geonames.org. This website always uses 'https://', but our data frequently has 'http://' in the URI without the 's'. To fix this, we want to select just that part of the string to edit, so we use Regex. It looksl ike this in the yaml:

```yaml
fixes:
  # fix location using http over https
  - type: regex_replace
    column: location
    pattern: '^http://'
    replacement: 'https://'
```
Here we choose the part of the value to replace (we are only taking the 'http://' part) and give the replacement, which is just 'https://'. Notice that the whole link is much more than this, it's something like 'http://sws\.geonames\.org/1234567', but we only care about the start and so we only select that in the pattern. Only values in the pattern will be edited by the replacement. This is why we use Regex -- we want to be able to select the relevant parts and leave other parts, especially those that could be different every time like IDs, alone. 

Another example of regex_replace is if we wanted to append a file extension to the end of a cell. In uo-athletics, the 'file' field should always end in .tif. But the data often is missing the extension. We can use regex_replace to append .tif to the end like so:

```yaml
fixes:
  # fix file column missing file extension (append .tif to the end of the ID)
  - type: regex_replace
    column: file
    pattern: '^(.*?)(?<!\.tif)$'
    replacement: '\1.tif'
```
WARNING: you **must** exclude values from the pattern that you don't want to append to. '.tif' is excluded to prevent '.tif.tif' results.

Notice that we are specifically *excluding* values that already end in '.tif'. Imagine if half of the cells in the column ended in '.tif', and half didn't. If we applied the fix to every cell in the column, we would end up with a bunch of '.tif.tif' double extensions because it would append every time. So we use the negative look-ahead in Regex to make sure that we only include files that don't end in '.tif'. 

You can use these methods to fix most simple issues, and with some creativity they can do quite a lot. Anecdotally, for some of the more annoying uo-athletics fixes they've sped up fixing the metadata by ten times. But they can be a bit annoying to get right, so it's your choice to use this or not!

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
