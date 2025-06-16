import sys, requests, json

# to do
    # add # of works in importer to argv
    # report more helpful info -- all works there? how many missing? how many with no file sets? etc.

try:
    solrselect = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
    q = f"q=bulkrax_identifier_tesim:{int(sys.argv[1].strip())}"
    fl = "&fl=id,member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim"
    rows = "&rows=100"
    response = requests.get(f"{solrselect}{q}{fl}{rows}").json()
except:
    print("did you run as '$ python3 solr.py [importer #]'?")
    exit()

print(f">>> Solr query results for importer {sys.argv[1]}:")
print(f"{response['response']['numFound']} works found for importer # {sys.argv[1]}")

no_fileset = []
no_coll = []
coll_ids = [] # I don't currently do anything with this
for work in response['response']['docs']:
    # is this the best way to check?
    try:
        work['file_set_ids_ssim']
    except KeyError as e:
        no_fileset.append(work['id'])
    try:
        coll_ids.append(work['member_of_collection_ids_ssim'])
    except:
        no_coll.append(work['id'])
if len(no_fileset) >= 1:
    print(f"{len(no_fileset)} work(s) with no file set id in Solr:")
    for pid in no_fileset:
        print(pid)
else:
    print("all works have file set id")
# is my logic here sound??
if len(no_coll) == response['response']['numFound']:
    print("!!! no works added to a collection")
    pass
elif len(no_coll) >= 1:
    print("work(s) which are not in any collection:")
    for pid in no_coll:
        print(pid)
else:
    print("all works are member of collection id(s)") 
    # show coll ids??
    # and/or, check that all works in importer added to same coll??
# not sure I want this
# print(">>> query result docs:")
# print(json.dumps(response['response']['docs'], indent=4))
