from od2validation import Package
import sys
import logging
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logging (replaces print statements throughout codebase, including
# in od2validation.py lines that are called from this script)
# For more detailed debug information, change logging.INFO to logging.DEBUG
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)

logger = logging.getLogger(__name__)

try:
    processing = Package(sys.argv[1])
    # print(type(processing)) # check
    processing.print_filepaths()
    processing.check_headers()
    processing.get_headers_instructions()
    logger.info("✓ Validation complete")
except IndexError:
    print("(!!) command missing config file name (do not include file extension)")
    print("EXAMPLE:\n> python3 process.py uo-athletics")
