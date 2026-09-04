import re

COMPLEX_MODEL_VALUE = "generic"
COMPLEX_RESOURCE_TYPE_VALUE = "http://purl.org/dc/dcmitype/Collection"
FILESET_TYPE_VALUE = "fileset"

def base_header(header: str) -> str:
    """Return the base header without _X for an enumerated header"""
    return re.sub(r'_\d+$', '', header)

def is_complex(row) -> bool:
    """Return True if row is complex, False otherwise"""
    if "model" not in row or "resource_type" not in row:
        raise KeyError("Row does not contain column for 'model' or 'resource_type'")
    model = str(row.get("model")).lower()
    resource = str(row.get("resource_type")).lower()
    return model == COMPLEX_MODEL_VALUE.lower() and resource == COMPLEX_RESOURCE_TYPE_VALUE.lower()

def is_fileset(row) -> bool:
    """Return True if row is a file set, False otherwise"""
    if "model" not in row:
        raise KeyError("Row does not contain column for 'model")
    model = str(row.get("model")).lower()
    return model == FILESET_TYPE_VALUE