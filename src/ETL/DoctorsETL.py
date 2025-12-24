import pandas as pd
from services.DataExtractor import DataExtractor
from services.DataTransformer import DataTransformer
from services.DataValidator import DataValidator
from services.DataLoader import DataLoader
import logging

class DoctorsETL:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.loader = DataLoader()
        self.expected_columns = ['doctor_id','name','specialty']

    def run(self, input_path: str) -> pd.DataFrame:
        df = self.extractor.load_data(input_path)
        assert list(df.columns) == self.expected_columns, "Column names do not match expected values"
        df = df.rename(columns={'doctor_id': 'id'})

        for col in ['id']:
            df[col] = self.transformer.clean_id_column(df[col])

        df = self.validator.validate_not_null(df, 'id')

        df = self.validator.remove_duplicates(df)
        self.validator.null_summary(df)

        return df
