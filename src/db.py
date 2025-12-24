import psycopg2
from sqlalchemy import create_engine, text
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": "5432",
    "dbname": "healthtech"
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def get_sqlalchemy_engine():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        logger.error(f"Error creating SQLAlchemy engine: {e}")
        raise

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    commands = [
        """
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INT PRIMARY KEY,
            name VARCHAR(255),
            specialty VARCHAR(255)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS appointments (
            booking_id VARCHAR(50) PRIMARY KEY,
            patient_id INT,
            doctor_id INT,
            booking_date TIMESTAMP,
            status VARCHAR(50),
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        );
        """
    ]
    
    try:
        for command in commands:
            cur.execute(command)
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_db()
