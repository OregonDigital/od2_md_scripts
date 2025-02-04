
**to-dos**  
*see [uo-athletics_guide](https://uoregon.sharepoint.com/:w:/r/sites/O365_LIB_DigitalLibraryServices/Shared%20Documents/OD2_UOregon/_guides/uo-athletics_guide.docx?d=w709e55a2446549b7a995d87657488226&csf=1&web=1&e=HV05YE) for current manual QA steps*

*not collection-specific*  

- confirm match from file column in csv for file in files/
    - (!) different for metadata for compound objs!
- confirm no data in dmrec column
- columns taking IRIs
    - spaces before / after
    - missing '|'
    - `.html` at end of IRI string
- confirm no data in rows with no `file` value
- date is EDTF


*collection-specific*  
- UO Athletics
    - file values begin `PH395_UP`, end `.tif` (not `PHP`) / identifier values begin `PH395_UP` (not `PHP`)
    - **THEN** confirm filenames in csv and in files/ match
    - local_collection_name = http://opaquenamespace.org/ns/localCollectionName/UniversityPhotosPaulHarveyIV
    - local_collection_id = PH395 UP
    - photographer = http://opaquenamespace.org/ns/creator/HarveyPaulWIV
    - ... lots more that could be hard-coded:
        - has_finding_aid
        - photographer
        - license
        - ... ... 



**ideas / questions**  
- validate column headers - this could involve adding list of headers to colls data
- force match folder + file names / rename folders and files
- check encoding or otherwise avoid messed-up item titles
- check identifier strings based on collection? 
- There's lots of collection-specific stuff that *could* be done but...
- replace old file with new / summarize changes when replacing old file with new?
- (?) Python virtual environment for windows - for installing libraries etc.
    - See SO > [virtualenv in PowerShell?](https://stackoverflow.com/questions/1365081/virtualenv-in-powershell): "The latest version of virtualenv supports PowerShell out-of-the-box."
    - https://pypi.org/project/virtualenv/
    - https://virtualenv.pypa.io/en/latest/user_guide.html


**errors experienced**  
- file header in .xlsx as `file.tif`
    - ***could not change cell value in .xlsx or .csv file!?!?***  
    - checking *other* metadata headers would be good but would be different per collection...
- 

