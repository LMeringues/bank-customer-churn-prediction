import pandas as pd
import sqlalchemy 
import os
import urllib.request

DATA_URL = "https://raw.githubusercontent.com/LMeringues/bank-customer-churn-prediction/refs/heads/main/data/botswana_bank_customer_churn.csv"
LOCAL_PATH = "data/botswana_bank_customer_churn.csv"
DB_PATH = "sqlite:///database/bank_churn.db"
TABLE_NAME = "bank_customers"

def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(')', '').str.replace('(', '')
    return df


def download_data_if_needed():
    if os.path.exists(LOCAL_PATH):
        print(f"File was found: {LOCAL_PATH}")
        return
    
    print("File wasn't found. Downloading from GitHub...")
    try:
        os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
        urllib.request.urlretrieve(DATA_URL, LOCAL_PATH)
        print("Downloading was finished")
    except Exception as e:
        print(f"Downloading error: {e}")

def run_ingestion():
    """ ETL process performing"""

    download_data_if_needed()
    
    #Extracting
    df = pd.read_csv(LOCAL_PATH)
    print(f"{df.shape[0]} rows were extracted")

    #Transforming
    print(f"Old columns' names example {df.columns[:5]}")
    df = clean_columns(df)
    print(f"New columns' names example {df.columns[:5]}")

    #Loading
    print("Connecting to database...")
    engine  = sqlalchemy.create_engine(DB_PATH)
    print(f"Recording data to {TABLE_NAME}")
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    print("Success")

if __name__ == "__main__":
    run_ingestion()