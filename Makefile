PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip
SHELL := /bin/bash


.PHONY: help install up down etl queries run clean build-glue

help:
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make up        - Start Docker services (Postgres)"
	@echo "  make down      - Stop Docker services"
	@echo "  make etl       - Run the ETL process and load data to DB"
	@echo "  make queries   - Run the business questions SQL queries"
	@echo "  make run       - Run both ETL and queries"
	@echo "  make clean     - Remove temporary files and compiled Python files"
	@echo "  make build-glue - Package the ETL code for AWS Glue"

install:
	$(PIP) install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down

etl:
	@mkdir -p logs
	@set -o pipefail; \
	$(PYTHON) src/run_etl.py 2>&1 | tee -a logs/etl_pipeline.log


queries:
	@mkdir -p logs
	@echo "Running Query 1: Most confirmed appointments" | tee -a logs/etl_pipeline.log
	docker exec -i healthtech_postgres psql -U user -d healthtech < sql/1_most_confirmed_doctor.sql 2>&1 | tee -a logs/etl_pipeline.log
	@echo "Running Query 2: Patient 34 confirmed" | tee -a logs/etl_pipeline.log
	docker exec -i healthtech_postgres psql -U user -d healthtech < sql/2_patient_34_confirmed.sql 2>&1 | tee -a logs/etl_pipeline.log
	@echo "Running Query 3: Cancelled appointments Oct 21-24" | tee -a logs/etl_pipeline.log
	docker exec -i healthtech_postgres psql -U user -d healthtech < sql/3_cancelled_oct_21_24.sql 2>&1 | tee -a logs/etl_pipeline.log
	@echo "Running Query 4: Total confirmed per doctor" | tee -a logs/etl_pipeline.log
	docker exec -i healthtech_postgres psql -U user -d healthtech < sql/4_confirmed_per_doctor.sql 2>&1 | tee -a logs/etl_pipeline.log

run: clean etl queries

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf logs

build-glue:
	cd src && python3 setup.py bdist_egg
	@echo "Package created at src/dist/"

