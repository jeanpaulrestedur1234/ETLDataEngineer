
import sys
import os
import logging
from unittest.mock import MagicMock, patch

# 1. Mock AWS Glue libraries BEFORE importing the script
sys.modules['awsglue'] = MagicMock()
sys.modules['awsglue.utils'] = MagicMock()

# Mock getResolvedOptions to return our local arguments
def mock_get_resolved_options(args, options):
    # Create dummy data for testing
    import pandas as pd
    
    doctors_data = {
        'doctor_id': [1, 2],
        'name': ['Dr. Strange', 'Dr. House'],
        'specialty': ['Magic', 'Diagnostic']
    }
    appointments_data = {
        'booking_id': [101, 102],
        'patient_id': [1, 2],
        'doctor_id': [1, 2],
        'booking_date': ['2023-11-01', '2023-11-02'],
        'status': ['Confirmed', 'Cancelled']
    }
    
    doc_path = 'tests/doctors.csv'
    app_path = 'tests/appointments.csv'
    
    pd.DataFrame(doctors_data).to_csv(doc_path, index=False)
    pd.DataFrame(appointments_data).to_csv(app_path, index=False)

    return {
        'DOCTORS_INPUT': doc_path,
        'APPOINTMENTS_INPUT': app_path,
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db'
    }

sys.modules['awsglue.utils'].getResolvedOptions = mock_get_resolved_options

# 2. Setup path to import glue_etl and src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# Also add src/ETL to path because legacy code imports 'services' directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/ETL')))

from dotenv import load_dotenv

def load_dotenv_safe():
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(env_path)

def test_glue_job_locally():
    print(">>> Setting up Local Glue Test Environment...")
    load_dotenv_safe()
    
    # Import the Glue Job script (it will use the mocks)
    import glue_job.glue_etl as glue_script
    
    # Overwrite the 'ETL' imports in glue_etl if needed, but since we added ../src to path
    # it should find the real ETL classes.
    
    print(">>> Running Glue Job Main Function...")
    try:
        # Patch the DataLoader to avoid writing to a real DB
        # We patch where it is imported/used. Since DataLoader is imported in DoctorsETL from services...
        # We can try patching 'src.ETL.services.DataLoader.DataLoader.load_to_db' if sys.modules structure matches.
        # Check Imports: glue_etl imports ETL.DoctorsETL. DoctorsETL imports services.DataLoader.
        
        # We patch 'services.DataLoader.DataLoader.load_to_db' because 'services' is imported as top-level
        with patch('services.DataLoader.DataLoader.load_to_db') as mock_db_load:
             glue_script.main()
             
        print(f"\n✅ SUCCESS: Local Glue Job Test passed! DB Load called {mock_db_load.call_count} times.")
    except Exception as e:
        print(f"\n❌ FAILED: Local Glue Job Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_glue_job_locally()
