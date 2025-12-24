import pandas as pd

class DataExtractor:
    def load_csv(self, path: str) -> pd.DataFrame:
        print(f"Loading data from {path}")
        df = pd.read_csv(path)
        print(f"Records loaded: {len(df)}")
        return df
