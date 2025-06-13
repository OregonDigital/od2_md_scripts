import sys, requests, json

# to do
    # add # of works in importer to argv
    # report more helpful info -- all works there? how many missing? how many with no file sets? etc.

try:
    solrselect = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
    q = f"q=bulkrax_identifier_tesim:{int(sys.argv[1].strip())}"
    fl = "&fl=member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim"
    rows = "&rows=100"
    response = requests.get(f"{solrselect}{q}{fl}{rows}")
    print(json.dumps(response.json(), indent=4))
except:
    print("did you run as '$ python3 solr.py [importer #]'?")
