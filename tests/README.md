# Tests

Simple integration tests for the OD2 metadata validation scripts.

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run a specific test file:
```bash
pytest tests/test_process.py
pytest tests/test_importer_solr.py
```

Run a specific test:
```bash
pytest tests/test_process.py::test_package_initializes
```

## Test Files

- **test_process.py** - Integration tests for the main validation workflow (process.py using od2validation.Package)
  - Tests Package initialization
  - Tests header validation
  - Tests CSV file loading
  - Tests that string validation catches mismatches (correctness)
  - Tests that regex validation catches invalid patterns (correctness)
  - Tests complete validation workflow (regression)
  - Tests validation on real test data (regression)

- **test_importer_solr.py** - Tests for Solr integration logic (importer-solr.py)
  - Tests Solr response parsing
  - Tests detection of missing file sets
  - Tests detection of missing collection IDs
  - Tests collection ID extraction

- **conftest.py** - Shared test fixtures
  - `test_filepaths_yaml` - Creates temporary filepaths_test.yaml for testing
  - `mock_solr_response` - Sample Solr response data for testing

## Adding a New Test

1. Open the appropriate test file (test_process.py or test_importer_solr.py)
2. Copy an existing test function
3. Rename it to start with `test_` and describe what it tests
4. Modify the test logic to test your specific case
5. Run the test to make sure it works: `pytest tests/test_process.py::your_test_name`

Example:
```python
def test_your_new_feature(test_filepaths_yaml):
    """Test description of what this tests."""
    package = Package("test", test=True)
    # Your test code here
    assert something == expected_value
```

## Test Data

Tests use the existing test data in the `test/` directory:
- `test/test.csv` - Sample metadata CSV file
- `test/files/` - Sample asset files

The test configuration is in `config/test.yaml`.

## Notes

- Tests should be independent - they can run in any order
- Each test should clearly show what it's testing (descriptive name and docstring)
- If a test fails, fix the code, not the test (unless the test is wrong)
- Add tests when you find bugs - write a test that catches the bug first

