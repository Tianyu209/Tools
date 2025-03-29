import pandas as pd
import argparse
def parquet_to_csv(file_path):
    df = pd.read_parquet(file_path)
    df.to_csv(file_path.replace('.parquet', '.csv'))
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Parquet file to CSV")
    parser.add_argument("file_path", help="Path to the Parquet file")
    args = parser.parse_args()

    parquet_to_csv(args.file_path)