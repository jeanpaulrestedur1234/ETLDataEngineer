import logging
import pandas as pd

class DataValidator:

    @staticmethod
    def validate_not_null(df: pd.DataFrame, column: str) -> pd.DataFrame:
        before = len(df)
        df = df.dropna(subset=[column])
        logging.info(f"Records after removing null {column}: {len(df)} ({before - len(df)} removed)")
        return df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        dupes = df.duplicated().sum()
        logging.info(f"Duplicate records detected: {dupes}")
        return df.drop_duplicates()

    @staticmethod
    def null_summary(df: pd.DataFrame):
        logging.info("\nNull values summary:")
        logging.info(df.isnull().sum())
