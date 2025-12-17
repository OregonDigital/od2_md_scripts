import sys, requests, json
from typing import List, Any

try:
    importer_no = int(sys.argv[1].strip())
    in_importer = int(sys.argv[2].strip())
    solrselect = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
    q = f"q=bulkrax_identifier_tesim:{importer_no}"
    fl = "&fl=id,member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim"
    rows = "&rows=1000"
    response = requests.get(f"{solrselect}{q}{fl}{rows}").json()
except:
    print("(!!) Run as follows:")
    print("python3 importer-solr.py [importer #] [# of works in importer package]")
    exit()

print(f"*** Solr query results for importer {sys.argv[1]}")
print(f"""{response['response']['numFound']} / {in_importer}
        works in Solr / works in importer # {importer_no}""")

no_file_set: List[str] = []
coll_ids: List[Any] = []
no_coll_id: List[str] = []

for work in response['response']['docs']:
    try:
        work['file_set_ids_ssim']
    except KeyError as e:
        no_file_set.append(work['id'])
    try:
        coll_id = work['member_of_collection_ids_ssim']
        if coll_id not in coll_ids:
            coll_ids.append(coll_id)
    except:
        no_coll_id.append(work['id'])

if len(no_file_set) >= 1:
    print(f"""(!!) {len(no_file_set)} / {response['response']['numFound']} 
            work(s) in Solr for importer {importer_no} have no file set id""")
    print("PID(s) for works missing file set id:")
    for pid in no_file_set:
        print(pid)
else:
    print(f"*** All {response['response']['numFound']} works in Solr have file set id")

if len(no_coll_id) == response['response']['numFound']:
    print(f"(!!) No works in Solr for importer {importer_no} are in collection(s)")
    pass
elif len(no_coll_id) >= 1:
    print(f"""(!!) {len(no_coll_id)} / {response['response']['numFound']} 
            work(s) in Solr for importer {importer_no} are not in any collection""")
    print(f"PID(s) for works not in any collection:")
    for pid in no_coll_id:
        print(pid)
else:
    print(f"""*** All {response['response']['numFound']} works in Solr 
            for importer {importer_no} are member of collection id(s)""")
if len(coll_ids) > 0:
    print("Parent collection id(s):")
    for id in coll_ids:
        print(id)

to_print = input("Print query response? y/n\n>>> ")
if to_print.lower() == "y":
    print("*** Solr query response")
    print(json.dumps(response, indent=4))
