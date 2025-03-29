# auto_convert.py

This script does the following:

1. **Folder Creation**: If the folders "csv" and "parquet" do not exist, it will create them in the same directory as the script.
2. **File Conversion**:
    - Converts all CSV files in the "csv" folder to Parquet files in the "parquet" folder.
    - Converts all Parquet files in the "parquet" folder to CSV files in the "csv" folder.

---

# gui.py

This script provides a GUI with two buttons for file and folder conversion:

1. **File Convert**:  
   Converts a single file (either CSV or Parquet) to the other format.

2. **Folder Convert**:  
   Converts all files in a selected folder (CSV or Parquet) to the other format:
   - CSV files will be stored in the "csv" folder.
   - Parquet files will be stored in the "parquet" folder.
