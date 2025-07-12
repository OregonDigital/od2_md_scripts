from od2validation import Package

# requires od2_md_scripts/filepaths_test.yaml, 
# which is .gitignored and may not exist locally,
# as:
# metadata:
#   - /path/to/od2_md_scripts/test/test.xlsx|csv
# assets: /path/to/od2_md_scripts/test/files

test = Package("test", True)
test.print_filepaths()
test.print_config()
test.print_headers()
test.check_headers()
test.get_headers_instructions()