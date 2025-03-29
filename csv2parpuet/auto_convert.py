import os
import pandas as pd


CSV_FOLDER = "csv"
PARQUET_FOLDER = "parquet"
os.makedirs(CSV_FOLDER, exist_ok=True)
os.makedirs(PARQUET_FOLDER, exist_ok=True)
def convert_csv_to_parquet():
    """Convert all CSV files in the csv/ folder to Parquet and save them in parquet/."""
    for file in os.listdir(CSV_FOLDER):
        if file.endswith(".csv"):
            csv_path = os.path.join(CSV_FOLDER, file)
            parquet_path = os.path.join(PARQUET_FOLDER, file.replace(".csv", ".parquet"))

            try:
                df = pd.read_csv(csv_path)
                df.to_parquet(parquet_path, index=False)
                print(f"Converted {file} → {os.path.basename(parquet_path)}")
            except Exception as e:
                print(f"Error converting {file}: {e}")

def convert_parquet_to_csv():
    """Convert all Parquet files in the parquet/ folder to CSV and save them in csv/."""
    for file in os.listdir(PARQUET_FOLDER):
        if file.endswith(".parquet"):
            parquet_path = os.path.join(PARQUET_FOLDER, file)
            csv_path = os.path.join(CSV_FOLDER, file.replace(".parquet", ".csv"))

            try:
                df = pd.read_parquet(parquet_path)
                df.to_csv(csv_path, index=False)
                print(f"Converted {file} → {os.path.basename(csv_path)}")
            except Exception as e:
                print(f"Error converting {file}: {e}")

if __name__ == "__main__":
    convert_csv_to_parquet()
    convert_parquet_to_csv()
    print("✅ Conversion completed!")
