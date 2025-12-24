import pandas as pd
from services.DataExtractor import DataExtractor
from services.DataTransformer import DataTransformer
from services.DataValidator import DataValidator
from services.DataLoader import DataLoader

class AppointmentsETL:

    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.loader = DataLoader()
        self.expected_columns = [
            'booking_id',
            'patient_id',
            'doctor_id',
            'booking_date',
            'status'
        ]

    def run(self, input_path: str) -> pd.DataFrame:
        
        df = self.extractor.load_data(input_path)
        

        assert list(df.columns) == self.expected_columns, \
            f"Column names do not match expected schema. Found: {list(df.columns)}"
        df = df.rename(columns={'booking_id': 'id'})

        for col in ['id', 'patient_id', 'doctor_id']:
            df[col] = self.transformer.clean_id_column(df[col])

        df = self.validator.validate_not_null(df, 'patient_id')

        df['booking_date'] = self.transformer.clean_date_column(df['booking_date'])

        df['status'] = self.transformer.normalize_status(df['status'])

        df = self.validator.remove_duplicates(df)
        self.validator.null_summary(df)

        return df
