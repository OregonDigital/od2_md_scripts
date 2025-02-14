import yaml, os, csv

class UOAIngest(object):


    def __init__(self):
        self.metadata = self.files_config()[0]
        self.assets = os.listdir(self.files_config()[1])
        self.config = self.fields_config()


    def files_config(self):
        with open("files_config.yaml", "r") as yamlfile:
            paths = yaml.safe_load(yamlfile)
            return [ paths['metadata'], paths['assets'] ]


    def fields_config(self):
        with open("config/uo-athletics_config.yaml", "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
            return(config)
    
    def all_csv_processing(self):
        with open(self.metadata, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # pause
                pass
