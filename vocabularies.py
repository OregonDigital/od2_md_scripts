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
    pattern = r'http:\/\/id\.loc\.gov\/authorities\/names\/(n|no|nr|nb)\d{8,10}'
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

def validate_lcsh(value: str) ->  bool:
    """Validate lcsh URI format
    
    Examples:
    from website: "http://id.loc.gov/authorities/subjects/sh85055245"
    from website: "http://id.loc.gov/authorities/subjects/sh85104841"
    od2 map: "http://id.loc.gov/authorities/subjects/sh85105182"
    TODO slightly suspicious that these all have the same starting 'sh' given that lcnaf didn't, and there's not very many examples in the solr select. Check more extensively 

    Match start through subjects/sh, then 8 digits
    """
    pattern = r'http:\/\/id\.loc\.gov\/authorities\/subjects\/sh\d{8}'
    return bool(re.match(pattern, value))

def validate_tgm(value: str) ->  bool:
    """Validate tgm URI format
    
    Examples:
    from website: "http://id.loc.gov/vocabulary/graphicMaterials/tgm003035"
    from website: "http://id.loc.gov/vocabulary/graphicMaterials/tgm009453"
    from website: "http://id.loc.gov/vocabulary/graphicMaterials/tgm003961"
    od2 map: "http://id.loc.gov/vocabulary/graphicMaterials/tgm007711"

    Match start through graphicMaterials/tgm, then 6 digits
    """
    pattern = r'http:\/\/id\.loc\.gov\/vocabulary\/graphicMaterials\/tgm\d{6}'
    return bool(re.match(pattern, value))

def validate_aat(value: str) ->  bool:
    """Validate aat URI format
    
    Examples:
    website: "http://vocab.getty.edu/aat/300011213"
    website: "http://vocab.getty.edu/aat/300185650"
    od2 map: "http://vocab.getty.edu/aat/300134977"

    Match start through aat/300, then 6 digits
    """
    pattern = r'http:\/\/vocab\.getty\.edu\/aat\/300\d{6}'
    return bool(re.match(pattern, value))

def validate_subject(value: str) ->  bool:
    """Validate subject URI format
    
    Examples:
    website: "http://opaquenamespace.org/ns/subject/BiddleMorelandAlice"
    website: "http://opaquenamespace.org/ns/subject/AutzenStadiumEugeneOr"
    od2 map: "http://opaquenamespace.org/ns/subject/Glasswork"

    Match start through subject/, then 1 or more letters
    TODO check if numbers are ok and if this is never empty
    """
    pattern = r'http:\/\/opaquenamespace\.org\/ns\/subject\/[a-zA-Z]+'
    return bool(re.match(pattern, value))

def validate_lcorgs(value: str) ->  bool:
    """Validate lcorgs URI format
    
    Examples:
    website: "http://id.loc.gov/vocabulary/organizations/orul"
    website: ""
    od2 map: "http://id.loc.gov/vocabulary/organizations/orumu"

    Match start through organizations/oru, then 1 or more letters
    TODO find more examples
    """
    pattern = r'http:\/\/id\.loc\.gov\/vocabulary\/organizations\/oru[a-zA-Z]+'
    return bool(re.match(pattern, value))

def validate_itis(value: str) ->  bool:
    """Validate itis URI format
    
    Examples:
    website: "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=82696"
    website: "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=563984"
    website: "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=175861"
    od2 map: "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=99208"

    Match start through search_value= and then 1 or more integers
    """
    pattern = r'https:\/\/www\.itis\.gov\/servlet\/SingleRpt\/SingleRpt\?search_topic=TSN&search_value=\d+'
    return bool(re.match(pattern, value))

def validate_ubio(value: str) ->  bool:
    """Validate ubio URI format
    
    Examples:

    Match start through ...
    """
    pattern = r''
    return bool(re.match(pattern, value))

def validate_osubuildings(value: str) ->  bool:
    """Validate osubuildings URI format
    
    Examples:

    Match start through ...
    """
    pattern = r''
    return bool(re.match(pattern, value))

def validate_lcgenreforms(value: str) ->  bool:
    """Validate lcsh lcgenreforms format
    
    Examples:

    Match start through ...
    """
    pattern = r''
    return bool(re.match(pattern, value))

def validate_bne(value: str) ->  bool:
    """Validate bne URI format
    
    Examples:

    Match start through ...
    """
    pattern = r''
    return bool(re.match(pattern, value))

def validate_homosaurus(value: str) ->  bool:
    """Validate homosaurus URI format
    
    Examples:

    Match start through ...
    """
    pattern = r''
    return bool(re.match(pattern, value))



VOCABULARY_VALIDATORS = {
    'lcnaf': validate_lcnaf,
    'ulan': validate_ulan,
    'creator': validate_creator,
    'people': validate_people,
    'wikidata': validate_wikidata,
    'osuacademicunits': validate_osuacademicunits,
    'lcsh': validate_lcsh,
    'tgm': validate_tgm,
    'aat': validate_aat,
    'subject': validate_subject,
    'lcorgs': validate_lcorgs,
    'itis': validate_itis,
    'ubio': validate_ubio,
    'osubuildings': validate_osubuildings,
    'lcgenreforms': validate_lcgenreforms,
    'bne': validate_bne,
    'homosaurus': validate_homosaurus
    # Add rest here
}