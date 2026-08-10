import re

def base_header(header: str) -> str:
    """Return the base header without _X for an enumerated header"""
    return re.sub(r'_\d+$', '', header)

def is_complex(row) -> bool:
    """Return True if row is complex, False otherwise"""
    #FIXME: Should the check be using model generic or format = xml link?
    return row.get("model").lower() == "generic"