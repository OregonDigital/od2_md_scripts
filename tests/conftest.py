"""Shared fixtures for tests."""
import os
import yaml
import pytest
import pandas as pd
from pathlib import Path

# Get the project root directory (parent of tests/)
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def temp_test_environment(tmp_path):
    """Create a temporary test environment with config and data files."""
    # Create config directory
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Create default config (minimal version)
    default_config = {
        'dmrec': [{'regex': r'^$', 'which': 'all'}],
        'file': [{'method': 'check_filenames_assets', 'args': ['file']}],
    }
    
    with open(config_dir / "default.yaml", "w") as f:
        yaml.dump(default_config, f)
    
    # Create test config
    test_config = {
        'dmrec': [{'regex': r'^coll123_\d+$', 'which': 'all'}],
        'file': [{'method': 'check_filenames_assets', 'args': ['file']}],
        'title': [{'regex': r'^.+$', 'which': 'all'}],
        'format': [
            {'string': 'image/jpeg', 'which': 'all'},
            {'string': 'application/pdf', 'which': 'all'}
        ],
        'resource_type': [
            {'string': 'Image', 'which': 'all'},
            {'string': 'Text', 'which': 'all'}
        ]
    }
    
    with open(config_dir / "test.yaml", "w") as f:
        yaml.dump(test_config, f)
    
    # Create validation_mappings config (needed by Package)
    validation_mappings = {}
    with open(config_dir / "validation_mappings.yaml", "w") as f:
        yaml.dump(validation_mappings, f)
    
    # Create test CSV
    test_data = pd.DataFrame({
        'dmrec': ['coll123_1', 'coll123_2', 'coll123_3'],
        'file': ['image001.jpg', 'image002.jpg', 'document001.pdf'],
        'title': ['Test Image One', 'Test Image Two', 'Test Document'],
        'format': ['image/jpeg', 'image/jpeg', 'application/pdf'],
        'resource_type': ['Image', 'Image', 'Text']
    })
    
    csv_path = tmp_path / "test_metadata.csv"
    test_data.to_csv(csv_path, index=False)
    
    # Create assets directory with test files
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    (assets_dir / "image001.jpg").touch()
    (assets_dir / "image002.jpg").touch()
    (assets_dir / "document001.pdf").touch()
    
    # Create filepaths.yaml
    filepaths_config = {
        'metadata': [str(csv_path)],
        'assets': str(assets_dir)
    }
    
    filepaths_yaml = tmp_path / "filepaths.yaml"
    with open(filepaths_yaml, "w") as f:
        yaml.dump(filepaths_config, f)
    
    # Temp directory for tests
    original_dir = Path.cwd()
    os.chdir(tmp_path)
    
    yield {
        'config_path': config_dir / "test.yaml",
        'csv_path': csv_path,
        'assets_dir': assets_dir,
        'filepaths_yaml': filepaths_yaml,
        'tmp_path': tmp_path
    }
    
    # Cleanup: change back to original directory
    os.chdir(original_dir)


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

