import pandas as pd
import numpy as np
import re

class DataTransformer:

    @staticmethod
    def clean_id_column(series: pd.Series) -> pd.Series:
        def clean_value(x):
            if pd.isna(x):
                return np.nan
            if isinstance(x, (int, np.integer)):
                return int(x)
            if isinstance(x, (float, np.floating)):
                return int(x)
            if isinstance(x, str):
                x = x.strip()
                x = re.sub(r'[^0-9\.]', '', x)
                if x == '':
                    return np.nan
                try:
                    return int(float(x))
                except ValueError:
                    return np.nan
            return np.nan

        return series.apply(clean_value).astype("Int64")

    @staticmethod
    def clean_date_column(series: pd.Series) -> pd.Series:
        def parse_date(x):
            if pd.isna(x):
                return pd.NaT

            x = str(x).strip()
            x = re.sub(r'[^0-9/-]', '', x)
            if x == '':
                return pd.NaT

            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', x):
                return pd.to_datetime(x, format='%Y-%m-%d', errors='coerce')

            if re.fullmatch(r'\d{4}/\d{2}/\d{2}', x):
                return pd.to_datetime(x, format='%Y/%m/%d', errors='coerce')

            if re.fullmatch(r'\d{2}-\d{2}-\d{4}', x):
                x = x.replace('-', '/')

            if re.fullmatch(r'\d{2}/\d{2}/\d{4}', x):
                return pd.to_datetime(x, format='%m/%d/%Y', errors='coerce')

            return pd.NaT

        return series.apply(parse_date)

    @staticmethod
    def normalize_status(series: pd.Series) -> pd.Series:
        return (
            series.astype(str)
            .str.lower()
            .str.replace(r'[^a-z]', '', regex=True)
            .str.replace(r'^cancel.*', 'cancelled', regex=True)
            .str.replace(r'^confirm.*', 'confirmed', regex=True)
        )
