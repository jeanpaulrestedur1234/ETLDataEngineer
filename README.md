# HealthTech ETL Pipeline

## Overview
This project is a local ETL (Extract, Transform, Load) pipeline designed to process doctor and appointment data from Excel files and load it into a PostgreSQL database. It is built using Python and Docker.

## Project Structure
```
ETLDataEngineer/
├── data/
│   └── raw/                # Raw input files (doctors.xlsx, appointments.xlsx)
├── logs/                   # Execution logs (etl_pipeline.log)
├── notebooks/              # Jupyter notebooks for EDA
├── sql/                    # SQL queries (split by business question)
│   ├── 1_most_confirmed_doctor.sql
│   ├── 2_patient_34_confirmed.sql
│   ├── 3_cancelled_oct_21_24.sql
│   └── 4_confirmed_per_doctor.sql
├── src/
│   ├── ETL/                # ETL Classes (DoctorsETL, AppointmentsETL, services)
│   ├── db.py               # Database connection and schema init
│   └── run_etl.py          # Main ETL pipeline script
├── docker-compose.yml      # PostgreSQL Docker configuration
├── Makefile                # Project orchestration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker & Docker Compose

### Data Preparation
Before running the pipeline, ensure your source files are placed in the correct directory:
-   **Directory**: `data/raw/`
-   **Files Required**:
    -   `doctors.xlsx`
    -   `appointments.xlsx`

*Note: The file paths are configurable via the `.env` file.*

### Environment Setup

#### 1. Virtual Environment
It is recommended to use a virtual environment to isolate dependencies.
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Configuration (.env)
Create a `.env` file in the project root to configure the database connection and file paths. You can use the provided `.env.example` as a template.

**Required Variables**:
```ini
# Database credentials
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=healthtech

# Data file paths
DOCTORS_INPUT=data/raw/doctors.xlsx
APPOINTMENTS_INPUT=data/raw/appointments.xlsx
```

### Quick Start with Makefile
The project uses a `Makefile` for easy orchestration.

1.  **Install Dependencies**:
    ```bash
    make install
    ```

2.  **Start Database**:
    ```bash
    make up
    ```

3.  **Run Full Pipeline (ETL + Queries)**:
    ```bash
    make run
    ```
    *This command runs the ETL process and executes the business queries, logging everything to `logs/etl_pipeline.log`.*

### Available Commands
-   `make install`: Install dependencies from requirements.txt.
-   `make up`: Start PostgreSQL container.
-   `make down`: Stop PostgreSQL container.
-   `make etl`: Run only the ETL process (`src/run_etl.py`).
-   `make queries`: Run only the SQL queries.
-   `make clean`: Remove temporary files (`__pycache__`).

### Logs
All execution outputs (ETL progress, SQL results, errors) are saved to:
`logs/etl_pipeline.log`

## Pipeline Explanation

### 1. Extract
- Reads `.xlsx` files using `pandas`.
- Logs the number of records extracted.

### 2. Transform
- **Cleaning**: Standardizes column names to lowercase.
- **Validation**:
    - Drops appointments with missing `patient_id`.
    - Converts `booking_date` to datetime objects.
- **Standardization**:
    - Normalizes `status` values to lowercase (e.g., 'Predicted' -> 'predicted', 'canceled' -> 'cancelled').
    - Ensures correct data types for IDs.
- **Data Integrity & Foreign Keys**:
    - The pipeline enforces **Referential Integrity** between Doctors and Appointments.
    - Since `appointments.doctor_id` is a Foreign Key referencing `doctors.id`, any appointment with a `doctor_id` that does not exist in the processed Doctors list is **effectively filtered out**.
    - This prevents database errors (`ForeignKeyViolation`) and ensures only valid appointments are loaded. These excluded records are logged for review.

### 3. Load
- **Target**: Local PostgreSQL database (`healthtech` schema).
- **Strategy**: Idempotent load using `TRUNCATE` + `INSERT`.
    - Tables are truncated with `CASCADE` to handle foreign keys.
    - Data is bulk inserted using `to_sql`.

## AWS Architecture Proposal
In a production environment on AWS, I would propose the following architecture:

| Stage | AWS Tool | Justification |
| :--- | :--- | :--- |
| **Extract** | **S3 + Lambda** | Upload raw Excel files to an S3 bucket. An S3 Event Trigger invokes a Lambda function to start processing. S3 provides durable logic storage, and Lambda is cost-effective for event-driven extraction. |
| **Transform** | **AWS Glue** | For scalable, serverless data integration. Glue jobs (Python/Spark) can handle complex transformations, schema evolution, and large datasets efficiently. For smaller datasets, Lambda with Pandas layers might suffice, but Glue is more robust for scaling. |
| **Load** | **Amazon RDS (PostgreSQL)** | Managed relational database service. Handles backups, patching, and scaling. Alternatively, **Amazon Redshift** if the goal is purely analytical warehousing with massive data volume. |
| **Orchestration** | **AWS Step Functions** | To coordinate the workflow (S3 -> Glue -> RDS) and handle retries/failures gracefully. |

