
import sys
import os
import pandas as pd
import logging
from awsglue.utils import getResolvedOptions
from sqlalchemy import create_engine

# Import from the packaged library
# Note: When running in Glue, we will pass the extra python files (zipped src)
# so 'ETL' should be importable if we set up paths correctly or install it.
# We will assume 'src' is the root of the package.
try:
    from ETL.DoctorsETL import DoctorsETL
    from ETL.AppointmentsETL import AppointmentsETL
except ImportError:
    # Handle the case where the zip is unzipped into a directory named 'src'
    sys.path.append('src')
    from ETL.DoctorsETL import DoctorsETL
    from ETL.AppointmentsETL import AppointmentsETL

def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    return logging.getLogger(__name__)

def get_engine(args):
    db_user = args['DB_USER']
    db_password = args['DB_PASSWORD']
    db_host = args['DB_HOST']
    db_port = args['DB_PORT']
    db_name = args['DB_NAME']
    
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)

def main():
    logger = setup_logging()
    
    # Get arguments
    args = getResolvedOptions(sys.argv, [
        'DOCTORS_INPUT', 
        'APPOINTMENTS_INPUT',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME'
    ])
    
    logger.info("Starting Glue ETL Job...")
    
    # Initialize Engine
    engine = get_engine(args)
    
    # 1. Doctors ETL
    logger.info("Running Doctors ETL...")
    doctors_etl = DoctorsETL()
    # DoctorsETL.run() loads data. In original code it expects a local path.
    # In Glue, if inputs are S3 paths (s3://...), Pandas read_csv/read_excel supports S3 URLs directly 
    # if s3fs is installed (which it usually is in Glue environment).
    try:
        df_doctors = doctors_etl.run(args['DOCTORS_INPUT'])
        doctors_etl.loader.load_to_db(df_doctors, 'doctors', engine)
    except Exception as e:
        logger.error(f"Doctors ETL Failed: {e}")
        raise e

    # 2. Appointments ETL
    logger.info("Running Appointments ETL...")
    appointments_etl = AppointmentsETL()
    try:
        df_appointments = appointments_etl.run(args['APPOINTMENTS_INPUT'])
        
        # Filter Logic (copied from run_etl.py main)
        if 'df_doctors' in locals():
            valid_doctor_ids = df_doctors['id'].unique()
            initial_count = len(df_appointments)
            df_appointments = df_appointments[df_appointments['doctor_id'].isin(valid_doctor_ids)]
            filtered_count = len(df_appointments)
            if initial_count != filtered_count:
                logger.warning(f"Filtered {initial_count - filtered_count} appointments with invalid doctor_ids.")
        
        appointments_etl.loader.load_to_db(df_appointments, 'appointments', engine)
    except Exception as e:
        logger.error(f"Appointments ETL Failed: {e}")
        raise e
        
    logger.info("Glue ETL Job Completed Successfully.")

if __name__ == "__main__":
    main()
