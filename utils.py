import re


def base_header(header: str) -> str:
    """Return the base header without _X for an enumerated header"""
    return re.sub(r'_\d+$', '', header)