"""URI validation functiosn for controlled vocabularies"""
import re
import logging

logger = logging.getLogger(__name__)

def validate_lcnaf(value: str) -> bool:
    """Validate lcnaf URI"""
    pattern = r''
    return bool(re.match(pattern, value))

def validate_ulan(value: str) -> bool:
    """Validate ULAN URI format"""
    pattern = r''
    return bool(re.match(pattern, value))

# Add rest here





VOCABULARY_VALIDATORS = {
    'lcnaf': validate_lcnaf,
    'ulan': validate_ulan
    # Add rest here
}