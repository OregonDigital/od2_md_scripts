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
    """Validate ulan URI format
    
    Examples:
    solr query: "http://vocab.getty.edu/ulan/500012467"
    solr query: "http://vocab.getty.edu/ulan/500006931"
    solr query: "http://vocab.getty.edu/ulan/500330183"
    od2 map: "http://vocab.getty.edu/ulan/500009666"
    
    Match start through ulan/, then 500, then 6 integers
    """
    # Examples
    pattern = r'http:\/\/vocab.getty.edu\/ulan\/500\d{6}'
    return bool(re.match(pattern, value))

def validate_creator(value: str) -> bool:
    """Validate creator URI format
    
    Examples:
    solr query: "http://opaquenamespace.org/ns/creator/HoldenDorbe"
    solr query: "http://opaquenamespace.org/ns/creator/Nexus"
    solr query: "http://opaquenamespace.org/ns/creator/OlsenandJohnson"
    solr query: "http://opaquenamespace.org/ns/creator/BennesJohnV"
    solr query: "http://opaquenamespace.org/ns/creator/OpsisArchitecturearchitecturalfirm"
    od2 map: "http://opaquenamespace.org/ns/creator/HaynesCharles"
    
    Match start through creator/, then any string with length > 0
    """
    pattern = r'http:\/\/opaquenamespace.org\/ns\/creator\/[a-zA-Z]+'
    return bool(re.match(pattern, value))

def validate_people(value: str) -> bool:
    """Validate people URI
    
    Examples:
    solr query: "http://opaquenamespace.org/ns/people/SkinnerJamesEdward18671959"
    solr query: "http://opaquenamespace.org/ns/people/SkinnerSusanLawrence18711952"
    solr query: "http://opaquenamespace.org/ns/people/SteinkeClaytonEJr"
    od2 map: "http://opaquenamespace.org/ns/people/GrayKen"

    Match start through people/, then any number of digits or letters with length > 0
    """
    pattern = r'http:\/\/opaquenamespace.org\/ns\/people\/[a-zA-Z\d]+'
    return bool(re.match(pattern, value))

def validate_wikidata(value: str) -> bool:
    """Validate wikidata URI format
    
    Examples:
    from website: "http://www.wikidata.org/entity/Q193020"
    od2 map: "http://www.wikidata.org/entity/Q6134558"
    
    Match start through entity/, then Q, then digits
    """
    pattern = r'http:\/\/www\.wikidata\.org\/entity\/Q\d+'
    return bool(re.match(pattern, value))

def validate_osuacademicunits(value: str) -> bool:
    """Validate osuacademicunits URI format
    
    Examples:
    from website: "http://opaquenamespace.org/ns/osuAcademicUnits/5eh7OKFX"
    from website: "http://opaquenamespace.org/ns/osuAcademicUnits/Sp8GIq9b"
    from website: "http://opaquenamespace.org/ns/osuAcademicUnits/LaningEnosRolandJr"
    od2 map: "http://opaquenamespace.org/ns/osuAcademicUnits/smuGLIjL"
    
    Match start through osuAcademicUnits/, then any number of digits or letters with length > 0 
    """
    pattern = r'http:\/\/opaquenamespace\.org\/ns\/osuAcademicUnits\/[a-zA-Z\d]+'
    return bool(re.match(pattern, value))

# Add rest here (from under each subfield of fields in controlled_vocab_map, in validation_mappings.yaml)





VOCABULARY_VALIDATORS = {
    'lcnaf': validate_lcnaf,
    'ulan': validate_ulan,
    'creator': validate_creator,
    'people': validate_people,
    'wikidata': validate_wikidata,
    'osuacademicunits': validate_osuacademicunits
    # Add rest here
}