"""Shared fixtures for tests."""
import os
import yaml
import pytest
from pathlib import Path

# Get the project root directory (parent of tests/)
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def test_filepaths_yaml():
    """Create a temporary filepaths_test.yaml in the project root for testing."""
    # Create filepaths_test.yaml content with absolute paths
    test_metadata_path = PROJECT_ROOT / "test" / "test.csv"
    test_assets_path = PROJECT_ROOT / "test" / "files"
    
    filepaths_content = {
        'metadata': [str(test_metadata_path)],
        'assets': str(test_assets_path)
    }
    
    # Write to project root (where Package class expects it)
    test_yaml_path = PROJECT_ROOT / "filepaths_test.yaml"
    with open(test_yaml_path, 'w') as f:
        yaml.dump(filepaths_content, f)
    
    yield test_yaml_path
    
    # Cleanup: remove the file after test
    if test_yaml_path.exists():
        test_yaml_path.unlink()


@pytest.fixture
def mock_solr_response():
    """Return a sample Solr response dictionary for testing."""
    return {
        'response': {
            'numFound': 3,
            'docs': [
                {
                    'id': 'test:work1',
                    'file_set_ids_ssim': ['test:fileset1'],
                    'member_of_collection_ids_ssim': ['test:collection1']
                },
                {
                    'id': 'test:work2',
                    'file_set_ids_ssim': ['test:fileset2'],
                    'member_of_collection_ids_ssim': ['test:collection1']
                },
                {
                    'id': 'test:work3',
                    # Missing file_set_ids_ssim to test error detection
                    'member_of_collection_ids_ssim': ['test:collection1']
                }
            ]
        }
    }

