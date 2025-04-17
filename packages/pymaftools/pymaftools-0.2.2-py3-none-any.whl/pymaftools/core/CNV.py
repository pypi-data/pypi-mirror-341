import pandas as pd
from .PivotTable import PivotTable

class CNV(PivotTable):
    @classmethod
    def read_CNV(cls, file_path):
        # TODO: read CNV and return CNV object
        return cls(df)
    
    @classmethod
    def read_gistic(cls, file_path, drop_cols=["Locus ID", "Cytoband"]):
        df = pd.read_csv(file_path, sep="\t")
        df = df.set_index(["Gene Symbol"])
        df = df.drop(drop_cols, axis=1)
        df.columns = df.columns.str.replace(".call", "")
        return cls(df)
    