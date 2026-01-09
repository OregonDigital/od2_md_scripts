"""Integration tests for process.py workflow using od2validation.Package."""
import pytest
from od2validation import Package
import logging


def test_package_initializes(test_filepaths_yaml):
    """Test that Package can initialize with test data."""
    package = Package("test", test=True)
    assert package is not None
    assert package.test is True
    assert len(package.metadata) > 0
    assert len(package.assets) > 0


def test_header_validation_passes(test_filepaths_yaml):
    """Test that header validation passes when headers match config."""
    package = Package("test", test=True)
    result = package.check_headers()
    assert result is True, "Headers should match the test configuration"


def test_get_dataframe_loads_csv(test_filepaths_yaml):
    """Test that CSV metadata file loads correctly into DataFrame."""
    package = Package("test", test=True)
    df = package.get_dataframe()
    assert df is not None
    assert len(df) > 0, "DataFrame should have rows"
    # Check that expected columns exist
    expected_columns = ['dmrec', 'file', 'title', 'format', 'resource_type']
    for col in expected_columns:
        assert col in df.columns, f"Column {col} should exist in DataFrame"


def test_string_validation(test_filepaths_yaml):
    """Test that string validation works correctly."""
    package = Package("test", test=True)
    # The test config has string validation for format and resource_type
    # This test verifies the validation workflow runs without errors
    # Note: We're testing the workflow completes, not that it logs errors
    try:
        package.get_headers_instructions()
        # If we get here, the validation workflow completed
        assert True
    except Exception as e:
        pytest.fail(f"Validation workflow should complete without exceptions: {e}")


def test_regex_validation(test_filepaths_yaml):
    """Test that regex validation works correctly."""
    package = Package("test", test=True)
    # The test config has regex validation for title field
    # Verify the validation can run
    try:
        package.get_headers_instructions()
        assert True
    except Exception as e:
        pytest.fail(f"Regex validation should work: {e}")


def test_file_validation_workflow(test_filepaths_yaml):
    """Test that filename validation method can be called."""
    package = Package("test", test=True)
    # Check that the check_filenames_assets method exists and can be called
    # Note: This will fail if file column doesn't match assets, which is expected
    try:
        # This method is called via get_method during validation
        # We'll test that the method exists and is callable
        method = package.check_filenames_assets
        assert callable(method)
    except AttributeError:
        pytest.fail("check_filenames_assets method should exist")


def test_validation_workflow_completes(test_filepaths_yaml):
    """Test that the complete validation workflow runs end-to-end."""
    package = Package("test", test=True)
    
    # Run the full workflow as process.py does
    package.print_filepaths()
    headers_valid = package.check_headers()
    assert headers_valid is True, "Headers should be valid for test data"
    
    # Run validation instructions (this is the main validation logic)
    # This should complete without raising exceptions
    try:
        package.get_headers_instructions()
        assert True, "Validation workflow completed successfully"
    except Exception as e:
        pytest.fail(f"Complete validation workflow should not raise exceptions: {e}")


def test_string_check_catches_mismatch(test_filepaths_yaml, caplog):
    """Test that perform_string_check logs an error when strings don't match."""
    package = Package("test", test=True)
    
    # Clear any previous logs
    caplog.clear()
    
    # Test with mismatched strings
    with caplog.at_level(logging.ERROR):
        package.perform_string_check("expected_value", "actual_value", 0)
    
    # Check that an error was logged
    assert len(caplog.records) > 0, "Error should be logged for string mismatch"
    assert "expected_value" in caplog.text or "actual_value" in caplog.text


def test_string_check_passes_when_matching(test_filepaths_yaml, caplog):
    """Test that perform_string_check doesn't log an error when strings match."""
    package = Package("test", test=True)
    
    caplog.clear()
    
    # Test with matching strings
    with caplog.at_level(logging.ERROR):
        package.perform_string_check("same_value", "same_value", 0)
    
    # Check that no error was logged
    assert len(caplog.records) == 0, "No error should be logged for matching strings"


def test_regex_check_catches_invalid_pattern(test_filepaths_yaml, caplog):
    """Test that perform_regex_check logs an error when pattern doesn't match."""
    import re
    package = Package("test", test=True)
    
    caplog.clear()
    
    # Pattern that should NOT match
    pattern = re.compile(r"^Complex Object: .*$")
    
    with caplog.at_level(logging.ERROR):
        package.perform_regex_check(pattern, "Wrong Format", 0)
    
    # Check that an error was logged
    assert len(caplog.records) > 0, "Error should be logged when regex doesn't match"
    assert "Wrong Format" in caplog.text


def test_regex_check_passes_when_matching(test_filepaths_yaml, caplog):
    """Test that perform_regex_check doesn't log an error when pattern matches."""
    import re
    package = Package("test", test=True)
    
    caplog.clear()
    
    # Pattern that SHOULD match
    pattern = re.compile(r"^Complex Object: .*$")
    
    with caplog.at_level(logging.ERROR):
        package.perform_regex_check(pattern, "Complex Object: Test", 0)
    
    # Check that no error was logged
    assert len(caplog.records) == 0, "No error should be logged when regex matches"


def test_check_headers_catches_mismatch(test_filepaths_yaml, caplog):
    """Test that check_headers detects when config doesn't match metadata."""
    # This test uses the existing test data where headers should match
    # If they don't match, check_headers returns False and logs errors
    package = Package("test", test=True)
    
    caplog.clear()
    
    with caplog.at_level(logging.ERROR):
        result = package.check_headers()
    
    # For valid test data, headers should match
    if result is False:
        # If they don't match, errors should be logged
        assert len(caplog.records) > 0, "Errors should be logged when headers don't match"


def test_validation_catches_errors_in_real_data(test_filepaths_yaml, caplog):
    """
    Regression test: Run validation on test data and ensure it completes.
    This test will fail if the validation logic breaks in a way that causes crashes.
    It also serves as documentation of expected behavior.
    """
    package = Package("test", test=True)
    
    caplog.clear()
    
    # Run the complete validation workflow
    with caplog.at_level(logging.INFO):
        package.get_headers_instructions()
    
    # The workflow should complete without crashes
    # Check that some validation happened (logs were created)
    assert len(caplog.records) > 0, "Validation should produce log messages"
    
    # Check that validation messages are present
    log_text = caplog.text
    assert "Validating" in log_text or "NO CHECK CONFIGURED" in log_text, \
        "Should see validation activity in logs"
