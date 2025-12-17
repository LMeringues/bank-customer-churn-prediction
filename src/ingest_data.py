import pandas as pd
import sqlalchemy 
import os

CSV_PATH = "data/botswana_bank_customer_churn.csv"
DB_PATH = "sqlite:///database/bank_churn.db"
TABLE_NAME = "bank_customers"

def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(')', '').str.replace('(', '')
    return df

def run_ingestion():
    """ ETL process performing"""

    #Extracting
    if not os.path.exists(CSV_PATH):
        print(f"File {CSV_PATH} wasn't found!")
        return

    df = pd.read_csv(CSV_PATH)
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