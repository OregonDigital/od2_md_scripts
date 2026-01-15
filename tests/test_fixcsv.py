"""Tests for fixcsv.py fix logic."""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path so we can import fixcsv
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import relevant functions from fixcsv
from fixcsv import (
    fix_strip_column,
    fix_regex_replace,
    fix_enforce_string,
    apply_collection_fixes
)

class TestFixStripColumn:
    """Tests for fix_strip_column function."""
    
    def test_strips_leading_whitespace(self):
        """Test that leading whitespace is removed."""
        df = pd.DataFrame({'title': [' text', '  more  ', 'clean']})
        result_df, changes = fix_strip_column(df, 'title')
        assert changes == 2
        assert result_df['title'].iloc[0] == 'text'
        assert result_df['title'].iloc[1] == 'more'
        assert result_df['title'].iloc[2] == 'clean'
    
    def test_strips_trailing_whitespace(self):
        """Test that trailing whitespace is removed."""
        df = pd.DataFrame({'title': ['text ', 'more  ', 'clean']})
        result_df, changes = fix_strip_column(df, 'title')
        assert changes == 2
        assert result_df['title'].iloc[0] == 'text'
        assert result_df['title'].iloc[1] == 'more'
    
    def test_strips_both_sides(self):
        """Test that whitespace on both sides is removed."""
        df = pd.DataFrame({'title': ['  text  ', ' word ']})
        result_df, changes = fix_strip_column(df, 'title')
        assert changes == 2
        assert result_df['title'].iloc[0] == 'text'
        assert result_df['title'].iloc[1] == 'word'
    
    def test_handles_clean_data(self):
        """Test that clean data results in zero changes."""
        df = pd.DataFrame({'title': ['clean', 'data', 'here']})
        result_df, changes = fix_strip_column(df, 'title')
        assert changes == 0
    
    def test_handles_missing_column(self):
        """Test that missing column is handled gracefully."""
        df = pd.DataFrame({'title': ['text']})
        result_df, changes = fix_strip_column(df, 'nonexistent')
        assert changes == 0
        assert len(result_df) == 1  # DataFrame unchanged
    
    def test_handles_nan_values(self):
        """Test that NaN values are skipped."""
        df = pd.DataFrame({'title': [' text ', None, pd.NA, '  word  ']})
        result_df, changes = fix_strip_column(df, 'title')
        assert changes == 2
        assert result_df['title'].iloc[0] == 'text'
        assert pd.isna(result_df['title'].iloc[1])
        assert pd.isna(result_df['title'].iloc[2])
        assert result_df['title'].iloc[3] == 'word'
    
    def test_preserves_internal_spaces(self):
        """Test that internal whitespace is preserved."""
        df = pd.DataFrame({'title': ['  hello world  ', ' multiple   spaces ']})
        result_df, changes = fix_strip_column(df, 'title')
        assert changes == 2
        assert result_df['title'].iloc[0] == 'hello world'
        assert result_df['title'].iloc[1] == 'multiple   spaces'


class TestFixRegexReplace:
    """Tests for fix_regex_replace function."""
    
    def test_replaces_http_with_https(self):
        """Test replacing http:// with https://."""
        df = pd.DataFrame({'url': ['http://example.com', 'http://test.org']})
        result_df, changes = fix_regex_replace(df, 'url', r'^http://', 'https://')
        assert changes == 2
        assert result_df['url'].iloc[0] == 'https://example.com'
        assert result_df['url'].iloc[1] == 'https://test.org'
    
    def test_no_change_when_pattern_not_found(self):
        """Test that no changes occur when pattern doesn't match."""
        df = pd.DataFrame({'url': ['https://example.com', 'ftp://test.org']})
        result_df, changes = fix_regex_replace(df, 'url', r'^http://', 'https://')
        assert changes == 0
    
    def test_replaces_with_capture_groups(self):
        """Test regex with capture groups."""
        df = pd.DataFrame({'url': ['http://sws.geonames.org/123/', 'http://sws.geonames.org/456/']})
        result_df, changes = fix_regex_replace(
            df, 'url', 
            r'^http://(sws\.geonames\.org/)', 
            r'https://\1'
        )
        assert changes == 2
        assert result_df['url'].iloc[0] == 'https://sws.geonames.org/123/'
        assert result_df['url'].iloc[1] == 'https://sws.geonames.org/456/'
    
    def test_handles_missing_column(self):
        """Test that missing column is handled gracefully."""
        df = pd.DataFrame({'url': ['http://example.com']})
        result_df, changes = fix_regex_replace(df, 'nonexistent', r'^http://', 'https://')
        assert changes == 0
    
    def test_handles_nan_values(self):
        """Test that NaN values are skipped."""
        df = pd.DataFrame({'url': ['http://example.com', None, pd.NA, 'http://test.org']})
        result_df, changes = fix_regex_replace(df, 'url', r'^http://', 'https://')
        assert changes == 2
        assert result_df['url'].iloc[0] == 'https://example.com'
        assert pd.isna(result_df['url'].iloc[1])
        assert pd.isna(result_df['url'].iloc[2])
        assert result_df['url'].iloc[3] == 'https://test.org'
    
    def test_replaces_multiple_occurrences(self):
        """Test replacing multiple occurrences in same string."""
        df = pd.DataFrame({'text': ['foo bar foo', 'foo baz']})
        result_df, changes = fix_regex_replace(df, 'text', r'foo', 'qux')
        assert changes == 2
        assert result_df['text'].iloc[0] == 'qux bar qux'
        assert result_df['text'].iloc[1] == 'qux baz'
    
    def test_complex_regex_pattern(self):
        """Test more complex regex patterns."""
        df = pd.DataFrame({'code': ['ABC-123', 'DEF-456', 'GHI789']})
        result_df, changes = fix_regex_replace(df, 'code', r'([A-Z]+)-(\d+)', r'\1_\2')
        assert changes == 2
        assert result_df['code'].iloc[0] == 'ABC_123'
        assert result_df['code'].iloc[1] == 'DEF_456'
        assert result_df['code'].iloc[2] == 'GHI789'  # No hyphen, no change


class TestFixEnforceString:
    """Tests for fix_enforce_string function."""
    
    def test_enforces_single_string_value(self):
        """Test that incorrect values are replaced with correct string."""
        df = pd.DataFrame({'license': ['wrong', 'incorrect', 'bad']})
        validation_config = {
            'license': [{'string': 'https://creativecommons.org/licenses/by-nc-nd/4.0/'}]
        }
        result_df, changes = fix_enforce_string(df, 'license', validation_config)
        assert changes == 3
        for i in range(3):
            assert result_df['license'].iloc[i] == 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
    
    def test_no_change_when_values_correct(self):
        """Test that correct values result in zero changes."""
        df = pd.DataFrame({'license': ['correct', 'correct', 'correct']})
        validation_config = {
            'license': [{'string': 'correct'}]
        }
        result_df, changes = fix_enforce_string(df, 'license', validation_config)
        assert changes == 0
    
    def test_handles_missing_column_in_config(self):
        """Test that missing column in config is handled gracefully."""
        df = pd.DataFrame({'license': ['value']})
        validation_config = {}
        result_df, changes = fix_enforce_string(df, 'license', validation_config)
        assert changes == 0
    
    def test_handles_no_string_rule(self):
        """Test that column with no string rule is skipped."""
        df = pd.DataFrame({'license': ['value']})
        validation_config = {
            'license': [{'regex': '^test$'}]  # No 'string' rule
        }
        result_df, changes = fix_enforce_string(df, 'license', validation_config)
        assert changes == 0
    
    def test_uses_first_string_rule(self):
        """Test that first string rule is used when multiple exist."""
        df = pd.DataFrame({'type': ['wrong', 'bad']})
        validation_config = {
            'type': [
                {'string': 'first_value'},
                {'string': 'second_value'}
            ]
        }
        result_df, changes = fix_enforce_string(df, 'type', validation_config)
        assert changes == 2
        assert result_df['type'].iloc[0] == 'first_value'
        assert result_df['type'].iloc[1] == 'first_value'
    
    def test_handles_nan_values(self):
        """Test that NaN values are skipped."""
        df = pd.DataFrame({'license': ['wrong', None, pd.NA, 'bad']})
        validation_config = {
            'license': [{'string': 'correct'}]
        }
        result_df, changes = fix_enforce_string(df, 'license', validation_config)
        assert changes == 2
        assert result_df['license'].iloc[0] == 'correct'
        assert pd.isna(result_df['license'].iloc[1])
        assert pd.isna(result_df['license'].iloc[2])
        assert result_df['license'].iloc[3] == 'correct'
    
    def test_partial_fix_when_some_correct(self):
        """Test that only incorrect values are changed."""
        df = pd.DataFrame({'license': ['correct', 'wrong', 'correct', 'bad']})
        validation_config = {
            'license': [{'string': 'correct'}]
        }
        result_df, changes = fix_enforce_string(df, 'license', validation_config)
        assert changes == 2
        for i in range(4):
            assert result_df['license'].iloc[i] == 'correct'


class TestApplyCollectionFixes:
    """Tests for apply_collection_fixes function."""
    
    def test_applies_single_strip_fix(self):
        """Test applying a single strip fix."""
        df = pd.DataFrame({'title': [' text ', 'clean', '  word  ']})
        fix_config = {
            'fixes': [
                {'type': 'strip', 'column': 'title'}
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 2
        assert result_df['title'].iloc[0] == 'text'
        assert result_df['title'].iloc[2] == 'word'
    
    def test_applies_single_regex_fix(self):
        """Test applying a single regex fix."""
        df = pd.DataFrame({'url': ['http://example.com', 'http://test.org']})
        fix_config = {
            'fixes': [
                {'type': 'regex_replace', 'column': 'url', 
                 'pattern': r'^http://', 'replacement': 'https://'}
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 2
        assert result_df['url'].iloc[0] == 'https://example.com'
    
    def test_applies_multiple_fixes(self):
        """Test applying multiple fixes in sequence."""
        df = pd.DataFrame({
            'title': [' text ', 'clean'],
            'url': ['http://example.com', 'http://test.org']
        })
        fix_config = {
            'fixes': [
                {'type': 'strip', 'column': 'title'},
                {'type': 'regex_replace', 'column': 'url',
                 'pattern': r'^http://', 'replacement': 'https://'}
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 3  # 1 strip + 2 regex
        assert result_df['title'].iloc[0] == 'text'
        assert result_df['url'].iloc[0] == 'https://example.com'
    
    def test_handles_unknown_fix_type(self):
        """Test that unknown fix types are skipped."""
        df = pd.DataFrame({'title': [' text ']})
        fix_config = {
            'fixes': [
                {'type': 'unknown_type', 'column': 'title'}
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 0
    
    def test_handles_missing_column_field(self):
        """Test that fix without column field is skipped."""
        df = pd.DataFrame({'title': [' text ']})
        fix_config = {
            'fixes': [
                {'type': 'strip'}  # Missing 'column'
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 0
    
    def test_handles_missing_regex_fields(self):
        """Test that regex fix without pattern/replacement is skipped."""
        df = pd.DataFrame({'url': ['http://example.com']})
        fix_config = {
            'fixes': [
                {'type': 'regex_replace', 'column': 'url'}  # Missing pattern and replacement
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 0
    
    def test_continues_after_failed_fix(self):
        """Test that failures don't stop subsequent fixes."""
        df = pd.DataFrame({
            'title': [' text '],
            'url': ['http://example.com']
        })
        fix_config = {
            'fixes': [
                {'type': 'strip'},  # Missing column - will fail
                {'type': 'regex_replace', 'column': 'url',
                 'pattern': r'^http://', 'replacement': 'https://'}  # Should still run
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 1
        assert result_df['url'].iloc[0] == 'https://example.com'
    
    def test_empty_fixes_list(self):
        """Test that empty fixes list results in zero changes."""
        df = pd.DataFrame({'title': [' text ']})
        fix_config = {'fixes': []}
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 0
    
    def test_real_world_uo_athletics_example(self):
        """Test realistic example from uo-athletics-fixes.yaml."""
        df = pd.DataFrame({
            'institution': ['University of Oregon ', 'UO  '],
            'license': ['http://creativecommons.org/licenses/by-nc/4.0/', 
                       'http://creativecommons.org/licenses/by-nc/4.0/'],
            'location': ['http://sws.geonames.org/5720727/', 
                        'http://sws.geonames.org/5720728/']
        })
        fix_config = {
            'fixes': [
                {'type': 'strip', 'column': 'institution'},
                {'type': 'regex_replace', 'column': 'location',
                 'pattern': r'^http://(sws\.geonames\.org/)',
                 'replacement': r'https://\1'}
            ]
        }
        result_df, total_changes = apply_collection_fixes(df, fix_config)
        assert total_changes == 4  # 2 strips + 2 regex
        assert result_df['institution'].iloc[0] == 'University of Oregon'
        assert result_df['institution'].iloc[1] == 'UO'
        assert result_df['location'].iloc[0] == 'https://sws.geonames.org/5720727/'
        assert result_df['location'].iloc[1] == 'https://sws.geonames.org/5720728/'


# Parametrized tests run test functions with different inputs -- basically
# repeats the existing tests but with a bunch more data to get better coverage
@pytest.mark.parametrize("input_data,expected_changes", [
    # No issues
    (['clean', 'data'], 0),
    # All need fixing
    ([' text ', '  word  ', ' more '], 3),
    # Mix of clean and dirty
    (['clean', ' text ', 'also clean', '  word  '], 2),
    # Empty string
    (['', ' ', '  '], 2),  # Empty string is already clean
])
def test_strip_parametrized(input_data, expected_changes):
    """Parametrized test for various strip scenarios."""
    df = pd.DataFrame({'title': input_data})
    result_df, changes = fix_strip_column(df, 'title')
    assert changes == expected_changes


@pytest.mark.parametrize("pattern,replacement,input_val,expected_val,should_change", [
    (r'^http://', 'https://', 'http://example.com', 'https://example.com', True),
    (r'^http://', 'https://', 'https://example.com', 'https://example.com', False),
    (r'foo', 'bar', 'foo test foo', 'bar test bar', True),
    (r'\d+', 'X', 'test123', 'testX', True),
    (r'\d+', 'X', 'testABC', 'testABC', False),
])
def test_regex_parametrized(pattern, replacement, input_val, expected_val, should_change):
    """Parametrized test for various regex scenarios."""
    df = pd.DataFrame({'field': [input_val]})
    result_df, changes = fix_regex_replace(df, 'field', pattern, replacement)
    assert changes == (1 if should_change else 0)
    assert result_df['field'].iloc[0] == expected_val