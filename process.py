import OdPackage

processing = OdPackage.Package()
metadata = processing.get_files_md()[0]
assets = processing.get_files_md()[1]
processing.check_assets_filenames(metadata, assets)
