from od2validation import Package
import sys
import logging
from typing import Dict
import re

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

# Track validation errors by header
error_count = 0
current_header = None
headers_with_errors = set()
validated_headers = []

class ErrorTrackingHandler(logging.Handler):
    """Handler to track which headers have errors"""
    # emit() is called automatically by logger for every log
    def emit(self, record):
        global error_count, current_header
        
        # Detect when we're validating a new header
        if record.levelno == logging.INFO and "Validating" in record.msg:
            # Extract header name from message like "Validating 'title' from config..."
            match = re.search(r"Validating '([^']+)'", record.msg)
            if match:
                current_header = match.group(1)
                if current_header not in validated_headers:
                    validated_headers.append(current_header)
        
        # Track errors for current header
        if record.levelno >= logging.ERROR and current_header:
            error_count += 1
            headers_with_errors.add(current_header)

# Add error tracking handler
logging.getLogger().addHandler(ErrorTrackingHandler())

try:
    collection_name = sys.argv[1]
    processing = Package(collection_name)
    processing.print_filepaths()
    processing.check_headers()
    processing.get_headers_instructions()
    
    logger.info("-- Validation complete --")
    if error_count == 0:
        logger.info ("No errors found")
    # Show fixcsv.py suggestion if errors were found
    else:
        logger.warning("\n" + "="*60)
        logger.warning(f"Validation found {error_count} error(s) in {len(headers_with_errors)}/{len(validated_headers)} headers")
        logger.warning(f"Headers with errors: {', '.join(sorted(headers_with_errors))}")
        logger.warning("")
        logger.warning("To automatically fix common issues:")
        logger.warning(f"  python3 fixcsv.py {collection_name}")
        logger.warning("="*60)
    
except IndexError:
    logger.error("Missing config file name (do not include file extension)")
    logger.error("EXAMPLE: python3 process.py uo-athletics")
