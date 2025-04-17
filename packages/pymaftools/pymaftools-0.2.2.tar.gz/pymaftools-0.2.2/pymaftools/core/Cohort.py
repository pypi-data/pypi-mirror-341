import pandas as pd
import pickle
import copy
from .PivotTable import PivotTable

class Cohort:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.tables = {}
        self.sample_metadata = None

    def add_table(self, table_name, table: PivotTable):
        if not isinstance(table, PivotTable):
            raise TypeError(f"Assay data for '{table_name}' must be an instance of PivotTable.")
        self.tables[table_name] = table
        
        if self.sample_metadata is None:
            self.sample_metadata = table
        else:
            # merge sample metadata
            if not table.sample_metadata.index.equals(self.sample_metadata.index):
                raise ValueError(f"Sample metadata index for '{table_name}' does not match sample metadata index of the cohort.")
            
            # find columns that are not in the cohort sample metadata
            new_columns = set(table.sample_metadata.columns) - set(self.sample_metadata.columns)
            if len(new_columns) > 0:
                self.sample_metadata = pd.concat([self.sample_metadata, table.sample_metadata[new_columns]], axis=1)

    def add_sample_metadata(self, sample_metadata: pd.DataFrame):
        if not isinstance(sample_metadata, pd.DataFrame):
            raise TypeError("Sample metadata must be a pandas DataFrame.")
        self.sample_metadata = sample_metadata

    def remove_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]

    def subset(self, 
        samples: list = []
        ):
        
        cohort = self.copy()
        for table_name, table in cohort.tables.items():
            cohort.tables[table_name] = table.subset(samples=samples)
        
        # subset sample_metadata
        cohort.sample_metadata = cohort.sample_metadata.loc[samples, :].copy()
        return cohort
            
    def copy(self, deep=True):
        new_instance = Cohort(self.name, self.description)
        new_instance.tables = copy.deepcopy(self.tables) if deep else self.tables.copy()
        new_instance.sample_metadata = (
            self.sample_metadata.copy(deep=True) if deep and self.sample_metadata is not None else self.sample_metadata
        )
        return new_instance

    def to_pickle(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
        print(f"Data saved to {file_path}.")

    @classmethod
    def read_pickle(cls, file_path):
        with open(file_path, 'rb') as f:
            cohort_instance = pickle.load(f)
        return cohort_instance