import pandas as pd
from db import get_sqlalchemy_engine

def run_queries():
    engine = get_sqlalchemy_engine()
    
    queries = {
        "1. Doctor with most confirmed appointments": """
            SELECT 
                d.name, 
                COUNT(a.booking_id) as confirmed_appointments
            FROM doctors d
            JOIN appointments a ON d.doctor_id = a.doctor_id
            WHERE a.status = 'confirmed'
            GROUP BY d.name
            ORDER BY confirmed_appointments DESC
            LIMIT 1;
        """,
        "2. Confirmed appointments for patient '34'": """
            SELECT 
                COUNT(booking_id) as patient_34_confirmed_count
            FROM appointments
            WHERE patient_id = 34 AND status = 'confirmed';
        """,
        "3. Cancelled appointments between 2025-10-21 and 2025-10-24": """
            SELECT 
                COUNT(booking_id) as cancelled_count
            FROM appointments
            WHERE status = 'cancelled'
              AND booking_date >= '2025-10-21 00:00:00'
              AND booking_date <= '2025-10-24 23:59:59';
        """,
        "4. Total confirmed appointments per doctor": """
            SELECT 
                d.name, 
                COUNT(a.booking_id) as total_confirmed
            FROM doctors d
            LEFT JOIN appointments a ON d.doctor_id = a.doctor_id AND a.status = 'confirmed'
            GROUP BY d.name
            ORDER BY total_confirmed DESC;
        """
    }
    
    print("--- Business Question Results ---")
    for question, sql in queries.items():
        print(f"\n{question}")
        try:
            df = pd.read_sql(sql, engine)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Error executing query: {e}")

if __name__ == "__main__":
    run_queries()
