import pandas as pd
import os
import logging

class DataLoader:
    def to_csv(self, df: pd.DataFrame, path: str):
        logging.info(f"Saving data to {path}")
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        logging.info("Data saved successfully.")

    def load_to_db(self, df: pd.DataFrame, table_name: str, engine):
        logging.info(f"Loading data to table {table_name}")
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logging.info(f"Data loaded to {table_name} successfully.")
