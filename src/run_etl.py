import sys
import os
import pandas as pd
import logging
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'ETL'))

from ETL.DoctorsETL import DoctorsETL
from ETL.AppointmentsETL import AppointmentsETL
from db import init_db, get_sqlalchemy_engine

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'etl_pipeline.log')
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Add handler to root logger
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)

def validate_paths(doctors_path, appointments_path):
    missing = []
    if not doctors_path or not os.path.exists(doctors_path):
        missing.append(f"Doctors file not found at: {doctors_path}")
    if not appointments_path or not os.path.exists(appointments_path):
        missing.append(f"Appointments file not found at: {appointments_path}")
    
    if missing:
        error_msg = "\n".join(missing)
        logging.error(f"Configuration Error:\n{error_msg}\nPlease check check your .env file and ensure DOCTORS_INPUT and APPOINTMENTS_INPUT variables are correct.")
        print(f"❌ ERROR: Input files not found!\n{error_msg}")
        return False
    return True

def validate_db_connection():
    try:
        init_db()
        return True
    except Exception as e:
        msg = f"Database connection failed: {e}\nPlease check your .env DB variables (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)."
        logging.error(msg)
        print(f"❌ ERROR: {msg}")
        return False

def main():
    setup_logging()
    load_dotenv()
    
    # Get Paths from environment
    doctors_input = os.getenv('DOCTORS_INPUT')
    appointments_input = os.getenv('APPOINTMENTS_INPUT')

    # Validate Paths
    if not validate_paths(doctors_input, appointments_input):
        sys.exit(1)

    # Validate DB
    logging.info("Initializing Database...")
    if not validate_db_connection():
        sys.exit(1)
        
    engine = get_sqlalchemy_engine()

    # Doctors ETL
    logging.info("\nRunning Doctors ETL...")
    doctors_etl = DoctorsETL()
    try:
        df_doctors = doctors_etl.run(doctors_input)
        # Load to DB
        doctors_etl.loader.load_to_db(df_doctors, 'doctors', engine)
    except Exception as e:
        logging.error(f"Doctors ETL Failed: {e.__str__()}")
        import traceback
        traceback.print_exc()

    logging.info("\nRunning Appointments ETL...")
    appointments_etl = AppointmentsETL()
    try:
        df_appointments = appointments_etl.run(appointments_input)
        

        if 'df_doctors' in locals():
            valid_doctor_ids = df_doctors['id'].unique()
            initial_count = len(df_appointments)
            df_appointments = df_appointments[df_appointments['doctor_id'].isin(valid_doctor_ids)]
            filtered_count = len(df_appointments)
            logging.info(f"Filtered {initial_count - filtered_count} appointments with invalid doctor_ids.")

  
        appointments_etl.loader.load_to_db(df_appointments, 'appointments', engine)
    except Exception as e:
        logging.error(f"Appointments ETL Failed: {e.__str__()}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
