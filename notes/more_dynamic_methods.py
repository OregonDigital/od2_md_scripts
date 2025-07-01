def get_method(method_name, args):
    method_mapping = {
        'check_filenames_assets': check_filenames_assets,
        'identifier_file_match': identifier_file_match
    }
    try:
        method = method_mapping.get(method_name)
        if method:
            return method(args)
        else:
            print(f"method {method_name} not found")
    except Exception as e:
        print(f"error {e}")

def check_filenames_assets(args):
    print("method check_filenames_assets")
    print(f"args = {args}")

def identifier_file_match(args):
    print("method identifier_file_match")
    print(f"args = {args}")


get_method("check_filenames_assets", "whoa yeah")
get_method("identifier_file_match", ["one", 2, "III"])
