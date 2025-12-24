

import pandas as pd

class DataValidator:

    @staticmethod
    def validate_not_null(df: pd.DataFrame, column: str) -> pd.DataFrame:
        before = len(df)
        df = df.dropna(subset=[column])
        print(f"Records after removing null {column}: {len(df)} ({before - len(df)} removed)")
        return df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        dupes = df.duplicated().sum()
        print(f"Duplicate records detected: {dupes}")
        return df.drop_duplicates()

    @staticmethod
    def null_summary(df: pd.DataFrame):
        print("\nNull values summary:")
        print(df.isnull().sum())
