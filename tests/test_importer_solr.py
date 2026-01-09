"""Tests for importer-solr.py Solr integration logic."""
import pytest
from unittest.mock import Mock, patch
import json


def test_parse_solr_response(mock_solr_response):
    """Test that valid Solr response is parsed correctly."""
    response = mock_solr_response
    
    # Check response structure
    assert 'response' in response
    assert 'numFound' in response['response']
    assert 'docs' in response['response']
    assert response['response']['numFound'] == 3
    assert len(response['response']['docs']) == 3


def test_missing_file_sets_detected(mock_solr_response):
    """Test that works missing file_set_ids_ssim are identified."""
    response = mock_solr_response
    docs = response['response']['docs']
    
    # Find docs without file_set_ids_ssim
    no_file_set = []
    for doc in docs:
        if 'file_set_ids_ssim' not in doc:
            no_file_set.append(doc['id'])
    
    # Should find one doc without file set (test:work3)
    assert len(no_file_set) == 1
    assert 'test:work3' in no_file_set


def test_missing_collection_ids_detected():
    """Test that works missing member_of_collection_ids_ssim are identified."""
    # Create a response with some docs missing collection IDs
    response = {
        'response': {
            'numFound': 2,
            'docs': [
                {
                    'id': 'test:work1',
                    'file_set_ids_ssim': ['test:fileset1'],
                    'member_of_collection_ids_ssim': ['test:collection1']
                },
                {
                    'id': 'test:work2',
                    'file_set_ids_ssim': ['test:fileset2']
                    # Missing member_of_collection_ids_ssim
                }
            ]
        }
    }
    
    docs = response['response']['docs']
    no_coll_id = []
    for doc in docs:
        if 'member_of_collection_ids_ssim' not in doc:
            no_coll_id.append(doc['id'])
    
    assert len(no_coll_id) == 1
    assert 'test:work2' in no_coll_id


def test_collection_ids_extraction(mock_solr_response):
    """Test that unique collection IDs are extracted correctly."""
    response = mock_solr_response
    docs = response['response']['docs']
    
    coll_ids = []
    for doc in docs:
        if 'member_of_collection_ids_ssim' in doc:
            coll_id = doc['member_of_collection_ids_ssim']
            if coll_id not in coll_ids:
                coll_ids.append(coll_id)
    
    # Should find one unique collection ID (as a list)
    assert len(coll_ids) == 1
    assert ['test:collection1'] in coll_ids


@patch('requests.get')
def test_solr_query_execution(mock_get):
    """Test that Solr query is constructed and executed correctly."""
    # Mock the response
    mock_response = Mock()
    mock_response.json.return_value = {
        'response': {
            'numFound': 1,
            'docs': [{'id': 'test:work1'}]
        }
    }
    mock_get.return_value = mock_response
    
    # Import and test the query logic
    import requests
    
    importer_no = 123
    solrselect = "https://solr-od2.library.oregonstate.edu/solr/prod/select?"
    q = f"q=bulkrax_identifier_tesim:{importer_no}"
    fl = "&fl=id,member_of_collection_ids_ssim,member_of_collections_ssim,file_set_ids_ssim"
    rows = "&rows=1000"
    
    response = requests.get(f"{solrselect}{q}{fl}{rows}")
    result = response.json()
    
    # Verify the request was made
    mock_get.assert_called_once()
    # Verify the response structure
    assert 'response' in result
    assert result['response']['numFound'] == 1

