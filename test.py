from od2ingest import Ingest

try:
    testing = Ingest("test", True)
    headers_match = testing.check_columns_config()
    if headers_match == True:
        testing.process_columns()
except IndexError as e:
    print(f"(!) {e}")