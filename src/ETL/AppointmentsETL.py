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

    def run(self, input_path: str, output_path: str) -> pd.DataFrame:

        df = self.extractor.load_csv(input_path)

        for col in ['booking_id', 'patient_id', 'doctor_id']:
            df[col] = self.transformer.clean_id_column(df[col])

        df = self.validator.validate_not_null(df, 'patient_id')

        df['booking_date'] = self.transformer.clean_date_column(df['booking_date'])
        df = self.validator.validate_not_null(df, 'booking_date')

        df['status'] = self.transformer.normalize_status(df['status'])

        df = self.validator.remove_duplicates(df)
        self.validator.null_summary(df)

        self.loader.to_csv(df, output_path)

        return df
