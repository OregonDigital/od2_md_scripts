import os

class Folder(object):

    all_files = []
    folders_files_manifest = {}
    file_extensions = [
        "pdf",
        "tif",
        "jpg" # may need more eventually
    ]
    libfiles_metadata = "L:\\DigitalProjects\\Metadata\\"

    def __init__(self, libfiles_metadata_folder):
        self.libfiles_metadata_folder = libfiles_metadata_folder
    
    def get_folders_files(self):
        target_dir = f"{self.libfiles_metadata}/{self.libfiles_metadata_folder}" # this doesn't work
        print(os.listdir(target_dir)) # test
        for item in target_dir:
            if item.split('.')[-1] == item or item.split('.')[-1] not in self.file_extensions:
                pass
