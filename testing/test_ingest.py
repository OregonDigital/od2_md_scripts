import pandas as pd

class FieldValues:
    def __init__(self, values):
        # Split values by '|' and store them as a list
        self.values = values.split('|') if isinstance(values, str) else [values]

class Ingest:
    def __init__(self, dataframe):
        # Dynamically create attributes for each column in the dataframe
        for column in dataframe.columns:
            setattr(self, column, FieldValues(dataframe[column].tolist()))

    def validate(self):
        # Example validation method
        for attr, value in self.__dict__.items():
            print(f"Validating {attr}: {value.values}")