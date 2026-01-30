import sys, requests, json, argparse
import logging
from typing import List, Any, Dict



# Set up logging (level is set to INFO, format tells log how to display messages)
# format uses a weird syntax because logging uses older string format style
logging.basicConfig(
    level=logging.INFO,
    # Display the level of the log name (like INFO or DEBUG) and then the log message after whitespace
    format='%(levelname)s:     %(message)s'
)

# There can be multiple loggers -- this sets the name of this one to the module (__main__ if it's run directly)
# so it's clear where logs come from. If another module imported process, it would show as process rather than __main__
logger = logging.getLogger()

# Parse the input (this gets each argument and checks that it matches the 
# expected order and type. It checks for the print flag, which lets a simple
# if statement at the bottom call print if true)
parser = argparse.ArgumentParser(description='Query Solr for importer information')
parser.add_argument('importer_no', type=int, help='Importer number')
parser.add_argument('in_importer', type=int, help='Number of works in importer package')
parser.add_argument('--print-response', '-p', action='store_true', 
                    help='Print the full Solr query response')
args = parser.parse_args()

importer_no = args.importer_no
in_importer = args.in_importer

solrselect = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
q = f"q=bulkrax_identifier_tesim:{importer_no}"
fl = "&fl=id,member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim"
rows = "&rows=1000"

try:
    response = requests.get(f"{solrselect}{q}{fl}{rows}").json()
except Exception as e:
    logger.error(f"Error making Solr request: {e}")
    exit(1)

logger.info(f"Solr query results for importer {importer_no}")
logger.info(f"""{response['response']['numFound']} / {in_importer} works in Solr / works in importer # {importer_no}""")

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
    logger.error(f"""{len(no_file_set)} / {response['response']['numFound']} work(s) in Solr for importer {importer_no} have no file set id""")
    logger.error("PID(s) for works missing file set id:")
    for pid in no_file_set:
        logger.error(f"  {pid}")
else:
    logger.info(f"All {response['response']['numFound']} works in Solr have file set id")

if len(no_coll_id) == response['response']['numFound']:
    logger.error(f"No works in Solr for importer {importer_no} are in collection(s)")
    pass
elif len(no_coll_id) >= 1:
    logger.error(f"""{len(no_coll_id)} / {response['response']['numFound']} work(s) in Solr for importer {importer_no} are not in any collection""")
    logger.error(f"PID(s) for works not in any collection:")
    for pid in no_coll_id:
        logger.error(f"  {pid}")
else:
    logger.info(f"""All {response['response']['numFound']} works in Solr for importer {importer_no} are member of collection id(s)""")
if len(coll_ids) > 0:
    logger.info("Parent collection id(s):")
    for id in coll_ids:
        logger.info(f"  {id}")

if args.print_response:
    logger.info("Solr query response")
    print(json.dumps(response, indent=4))
