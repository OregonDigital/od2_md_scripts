🔺 **details**  

The angelus exports are located: 
```
\\libfiles.uoregon.edu\DigitalProjects\Metadata\SCUA_patron_scans\Oregon Digital\URIs to fix\2_exported\angelus-studio
```

- The doc "angelusMapPairs2" is the one with recto/verso/archival_object_ids that need to be plugged into all the exports "export_angelus-studio_from_collection_1" through "export_angelus-studio_from_collection_14". 
- I finished 15 (renamed export_angelus-studio_from_collection_15a); I started 1 (renamed export_angelus-studio_from_collection_1a). 
- You are welcome to save whatever you need to a different location while you work out code. Thank you so much!...

*Goals:*  
- Move data from angelusMapPairs2 into the exports.
    - recto = id
    - verso = children
    - archival_object_id= archival_object_id

🔺 **processing + testing**
- see scripting.ipynb
- testing
    - spot-check random values from [file].csv / against [file]_processed.csv
    - check recto/verso for title match in Oregon Digital using URLs below
    - (!) archival object IDs not checked for matches (!)

```
# recto URL
https://www.oregondigital.org/concern/images/[recto pid]
# verso url
https://www.oregondigital.org/concern/images/[verso pid]
```
