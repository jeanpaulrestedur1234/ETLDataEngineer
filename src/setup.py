from setuptools import setup, find_packages

setup(
    name="etl_pipeline",
    version="0.1",
    packages=find_packages(),
    py_modules=['db', 'run_etl']
)
