import sys, requests, json, argparse
import logging
from typing import List, Any, Dict
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    COLORS: Dict[str, str] = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Set up logging colors and handler
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])

# Parse the input (this gets )
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
