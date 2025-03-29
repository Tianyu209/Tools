import pandas as pd
import argparse
def csv_to_parpuet(file_path):
    df = pd.read_csv(file_path)
    df.to_parquet(file_path.replace('.csv', '.parquet'))
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Parquet file to CSV")
    parser.add_argument("file_path", help="Path to the Parquet file")
    args = parser.parse_args()
    csv_to_parpuet(args.file_path)