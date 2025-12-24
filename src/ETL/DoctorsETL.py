import pandas as pd

class DoctorsETL:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.loader = DataLoader()

    def run(self, input_path: str, output_path: str) -> pd.DataFrame:
        df = self.extractor.load_csv(input_path)

        for col in ['doctor_id']:
            df[col] = self.transformer.clean_id_column(df[col])

        df = self.validator.validate_not_null(df, 'doctor_id')

        df = self.validator.remove_duplicates(df)
        self.validator.null_summary(df)

        self.loader.to_csv(df, output_path)

        return df
