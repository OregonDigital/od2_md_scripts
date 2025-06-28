from od2validation import Package

test = Package("test", True)
test.print_filepaths()
test.print_config()
test.print_headers()
test.check_headers()
test.check_dataframe()