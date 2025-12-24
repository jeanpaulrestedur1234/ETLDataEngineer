import pandas as pd
import logging
class DataExtractor:
    def load_data(self, path: str) -> pd.DataFrame:
        logging.info(f"Loading data from {path}")
        if path.endswith('.xlsx') or path.endswith('.xls'):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        logging.info(f"Records loaded: {len(df)}")
        return df
