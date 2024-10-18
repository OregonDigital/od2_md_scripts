import os

class OdFolder:
    def __init__(self, path_to_top_folder, coll):
        self = self
        self.path_to_top_folder = path_to_top_folder
        self.coll = coll
    
    # blarfffff
    # def rename_top(self):
    #     # below could be done more elegantly... with re?
    #     path = self.path_to_top_folder.split('/')[0]
    #     foldername = self.path_to_top_folder.split('/')[-1]
    #     return foldername
    #     # newname = self.top_foldername.replace(' ', '_')
    #     # newname = newname.replace('(', '')
    #     # newname = newname.replace(')', '')
    #     # newname = newname.replace('&', '')
    #     # os.system(f"mv {self.top_foldername} {newname}")
    

