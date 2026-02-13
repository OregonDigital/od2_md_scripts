"""URI validation functiosn for controlled vocabularies"""
import re
import logging

logger = logging.getLogger(__name__)

def validate_lcnaf(value: str) -> bool:
    """Validate lcnaf URI
    
    Examples:
    solr query: "http://id.loc.gov/authorities/names/no2013038294"
    solr query: "http://id.loc.gov/authorities/names/nr99003467"
    solr query: "http://id.loc.gov/authorities/names/nb2005019894"
    od2 map: "http://id.loc.gov/authorities/names/n93112029"

    Match exact start from http through names/, then could be n or no or nr or nb, then 8-10 integers
    """
    pattern = r'^http:\/\/id\.loc\.gov\/authorities\/names\/(n|no|nr|nb)\d{8,10}$'
    return bool(re.match(pattern, value))

def validate_ulan(value: str) -> bool:
    """Validate ULAN URI format
    
    Examples:
    
    
    """
    # Examples
    pattern = r''
    return bool(re.match(pattern, value))

def validate_creator(value: str) -> bool:
    """Validate creator URI format"""
    pattern = r''
    return bool(re.match(pattern, value))

def validate_people(value: str) -> bool:
    """Validate lcnaf URI"""
    pattern = r''
    return bool(re.match(pattern, value))

def validate_wikidata(value: str) -> bool:
    """Validate ULAN URI format"""
    pattern = r''
    return bool(re.match(pattern, value))

def validate_osuacademicunits(value: str) -> bool:
    """Validate creator URI format"""
    pattern = r''
    return bool(re.match(pattern, value))

# Add rest here





VOCABULARY_VALIDATORS = {
    'lcnaf': validate_lcnaf,
    'ulan': validate_ulan,
    'creator': validate_creator,
    'people': validate_people,
    'wikidata': validate_wikidata,
    'osuacademicunits': validate_osuacademicunits
    # Add rest here
}