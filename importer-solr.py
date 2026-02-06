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


def build_solr_query_url(importer_no: int) -> tuple[str, Dict[str, str]]:
    """Create Solr query URL for a given importer"""
    base_url = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
    params = {
        'q': f'bulkrax_identifier_tesim:{importer_no}',
        'fl': 'id,member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim,thumbnail_path_ss,suppressed_bsi,workflow_state_name_ssim,visibility_ssi',
        'rows': '1000'
    }
    return base_url, params

# solrselect = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
# q = f"q=bulkrax_identifier_tesim:{importer_no}"
# fl = "&fl=id,member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim"
# rows = "&rows=1000"

# try:
#     response = requests.get(f"{solrselect}{q}{fl}{rows}").json()
# except Exception as e:
#     logger.error(f"Error making Solr request: {e}")
#     exit(1)

# logger.info(f"Solr query results for importer {importer_no}")
# logger.info(f"""{response['response']['numFound']} / {in_importer} works in Solr / works in importer # {importer_no}""")

# TODO: Ask BMR what docs meant here, what actually is response['response']['docs']?
def analyze_works(docs: List[Dict]) -> tuple[List[str], List[Any], List[str]]:
    """Check if works have missing file sets or collection membership
    
    Returns:
        Tuple of (works without file sets, collection IDS, works without collections)
    """
    no_file_set = []
    coll_ids = []
    no_coll_id =[]
    bad_thumbnail = []
    suppressed_works = []
    bad_workflow = []
    bad_visibility = []

    for work in docs:
        work_id = work['id']

        # Check for file set value
        if 'file_set_ids_ssim' not in work:
            no_file_set.append(work_id)

        # Check for collection value
        if 'member_of_collection_ids_ssim' in work:
            coll_id = work['member_of_collection_ids_ssim']
            if coll_id not in coll_ids:
                coll_ids.append(coll_id)
        else:
            no_coll_id.append(work_id)
        
        # Check thumbnail path format
        if 'thumbnail_path_ss' in work:
            thumbnail = work['thumbnail_path_ss']
            if not (thumbnail.startswith('/downloads/') and '?file=thumbnail' in thumbnail):
                bad_thumbnail.append(f"{work_id} (thumbnail: {thumbnail})")
        else:
            bad_thumbnail.append(f"{work_id} (no thumbnail)")
        
        # Check suppressed status
        if work.get('suppressed_bsi') == True:
            suppressed_works.append(work_id)
        
        # Check workflow state
        workflow_state = work.get('workflow_state_name_ssim', [])
        if not workflow_state:
            bad_workflow.append(f"{work_id} (empty)")
        elif workflow_state[0] not in ['deposited', 'pending_review']:
            bad_workflow.append(f"{work_id} ({workflow_state[0]})")
        
        # Check visibility
        visibility = work.get('visibility_ssi', '')
        if visibility == 'private':
            bad_visibility.append(f"{work_id} (private)")
    return no_file_set, coll_ids, no_coll_id, bad_thumbnail, suppressed_works, bad_workflow, bad_visibility


# no_file_set: List[str] = []
# coll_ids: List[Any] = []
# no_coll_id: List[str] = []

# for work in response['response']['docs']:
#     try:
#         work['file_set_ids_ssim']
#     except KeyError as e:
#         no_file_set.append(work['id'])
#     try:
#         coll_id = work['member_of_collection_ids_ssim']
#         if coll_id not in coll_ids:
#             coll_ids.append(coll_id)
#     except:
#         no_coll_id.append(work['id'])

def log_file_set_status(no_file_set: List[str], total_works: int) -> None:
    """Log status of file sets in works"""
    if no_file_set:
        logger.error(f"{len(no_file_set)} / {total_works} work(s) have no file set id")
        logger.error("PID(s) for works missing file set id:")
        for pid in no_file_set:
            logger.error(f"  {pid}")
    else:
        logger.info(f"All {total_works} works have file set id")

def log_collection_status(no_coll_id: List[str], coll_ids: List[Any], total_works: int, importer_no: int) -> None:
    """Log status of collection membership"""
    if len(no_coll_id) == total_works:
        logger.error(f"No works in importer {importer_no} are in collection(s)")
    elif no_coll_id:
        logger.error(f"{len(no_coll_id)} / {total_works} are NOT in collection(s)")
        logger.error("PID(s) for works are not in any collection:")
        for pid in sorted(no_coll_id):
            logger.error(f"  {pid}")
    else:
        logger.info(f"All {total_works} works are members of collection(s)")
    
    if coll_ids:
        logger.info("Parent collection id(s):")
        for coll_id in sorted(coll_ids):
            logger.info(f"  {coll_id}")

def log_thumbnail_status(bad_thumbnail: List[str], total_works: int) -> None:
    """Log status of thumbnail paths"""
    if bad_thumbnail:
        logger.error(f"{len(bad_thumbnail)} / {total_works} work(s) have missing or bad thumbnail paths")
        logger.error("Works with thumbnail issues:")
        for item in sorted(bad_thumbnail):
            logger.error(f"  {item}")
    else:
        logger.info(f"All {total_works} works have valid thumbnail paths")

def log_suppression_status(suppressed_works: List[str], total_works: int) -> None:
    """Log status of suppressed works"""
    if suppressed_works:
        logger.warning(f"{len(suppressed_works)} / {total_works} work(s) are suppressed (haven't been reviewed)")
        logger.warning("Suppressed PIDs:")
        for pid in sorted(suppressed_works):
            logger.warning(f"  {pid}")
    else:
        logger.info("No works are suppressed")

def log_workflow_status(bad_workflow: List[str], total_works: int) -> None:
    """Log status of workflow states"""
    if bad_workflow:
        logger.error(f"{len(bad_workflow)} / {total_works} work(s) have unexpected workflow states")
        logger.error("Works with workflow issues:")
        for item in sorted(bad_workflow):
            logger.error(f"  {item}")
    else:
        logger.info(f"All {total_works} works have valid workflow states")

def log_visibility_status(bad_visibility: List[str], total_works: int) -> None:
    """Log status of visibility settings"""
    if bad_visibility:
        logger.error(f"{len(bad_visibility)} / {total_works} work(s) have private visibility")
        logger.error("Works with visibility issues:")
        for item in sorted(bad_visibility):
            logger.error(f"  {item}")
    else:
        logger.info(f"All {total_works} works have correct visibility")

# if len(no_file_set) >= 1:
#     logger.error(f"""{len(no_file_set)} / {response['response']['numFound']} work(s) in Solr for importer {importer_no} have no file set id""")
#     logger.error("PID(s) for works missing file set id:")
#     for pid in no_file_set:
#         logger.error(f"  {pid}")
# else:
#     logger.info(f"All {response['response']['numFound']} works in Solr have file set id")

# if len(no_coll_id) == response['response']['numFound']:
#     logger.error(f"No works in Solr for importer {importer_no} are in collection(s)")
#     pass
# elif len(no_coll_id) >= 1:
#     logger.error(f"""{len(no_coll_id)} / {response['response']['numFound']} work(s) in Solr for importer {importer_no} are not in any collection""")
#     logger.error(f"PID(s) for works not in any collection:")
#     for pid in no_coll_id:
#         logger.error(f"  {pid}")
# else:
#     logger.info(f"""All {response['response']['numFound']} works in Solr for importer {importer_no} are member of collection id(s)""")
# if len(coll_ids) > 0:
#     logger.info("Parent collection id(s):")
#     for id in coll_ids:
#         logger.info(f"  {id}")

# if args.print_response:
#     logger.info("Solr query response")
#     print(json.dumps(response, indent=4))

def main():
    """Run file"""
    args = parser.parse_args()

    logger.info(f"Querying Solr for importer {args.importer_no}")

    # Query Solr
    base_url, params = build_solr_query_url(args.importer_no)
    try:
        response = requests.get(base_url, params=params, timeout=10).json()
    except requests.RequestException as e:
        logger.error(f"Error making Solr request: {e}")
        sys.exit(1)

    # Extract results
    num_found = response['response']['numFound']
    docs = response['response']['docs']

    logger.info(f"{num_found} / {args.in_importer} works in Solr / works in importer # {args.importer_no}")

    # Analyze works
    no_file_set, coll_ids, no_coll_id, bad_thumbnail, suppressed_works, bad_workflow, bad_visibility = analyze_works(docs)

    # Report results
    log_file_set_status(no_file_set, num_found)
    log_collection_status(no_coll_id, coll_ids, num_found, args.importer_no)
    log_thumbnail_status(bad_thumbnail, num_found)
    log_suppression_status(suppressed_works, num_found)
    log_workflow_status(bad_workflow, num_found)
    log_visibility_status(bad_visibility, num_found)

    # Print response if requested
    if args.print_response:
        logger.info("Full Solr query response:")
        print(json.dumps(response, indent=4))


if __name__ == "__main__":
    main()