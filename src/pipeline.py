from dagster import op, job
import subprocess

@op
def scrape():
    subprocess.run(["python", "src/scraper.py"], check=True)

@op
def load_raw():
    subprocess.run(["python", "src/load_raw.py"], check=True)

@op
def run_dbt():
    subprocess.run(["dbt", "run"], check=True)

@op
def run_yolo():
    subprocess.run(["python", "src/yolo_detect.py"], check=True)

@job
def medical_pipeline():
    scrape()
    load_raw()
    run_dbt()
    run_yolo()
