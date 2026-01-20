from od2validation import Package
import sys
import logging
from colorama import Fore, Style, init
from typing import Dict

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Custom formatter with colors (this is basically just extending the 
# regular logging formatter by presetting a bunch of values, so we
# don't have to later)
class ColoredFormatter(logging.Formatter):
    COLORS: Dict[str, str] = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    # Using built-in logging formatter (which gets its colors from colorama)
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logging (replaces print statements throughout codebase, including
# in od2validation.py lines that are called from this script)
# For more detailed debug information, change logging.INFO to logging.DEBUG
handler = logging.StreamHandler()
# ColoredFormatter takes argument that's passed to logging.Formatter. This uses 
# Python's %-style formatting, so %(levelname)s is replaced with log level (DEBUG, INFO, etc.)
# %(message)s is replaced with the actual log message
handler.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)

logger = logging.getLogger(__name__)

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
            import re
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
error_handler = ErrorTrackingHandler()
logging.getLogger().addHandler(error_handler)

try:
    collection_name = sys.argv[1]
    processing = Package(collection_name)
    processing.print_filepaths()
    processing.check_headers()
    processing.get_headers_instructions()
    
    logger.info("✓ Validation complete")
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
