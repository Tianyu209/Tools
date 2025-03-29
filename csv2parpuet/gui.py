import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
CSV_FOLDER = "csv"
PARQUET_FOLDER = "parquet"
os.makedirs(CSV_FOLDER, exist_ok=True)
os.makedirs(PARQUET_FOLDER, exist_ok=True)
def convert_file():
    """Single file selection and conversion."""
    file_path = filedialog.askopenfilename(title="Select a CSV or Parquet File",
                                           filetypes=[("CSV Files", "*.csv"), ("Parquet Files", "*.parquet")])

    if not file_path:
        return

    try:
        file_dir, file_name = os.path.split(file_path)
        if file_path.endswith(".csv"):
            output_file = os.path.join(file_dir, file_name.replace(".csv", ".parquet"))
            df = pd.read_csv(file_path)
            df.to_parquet(output_file, index=False)
            messagebox.showinfo("Success", f"Converted: {output_file}")
        elif file_path.endswith(".parquet"):
            output_file = os.path.join(file_dir, file_name.replace(".parquet", ".csv"))
            df = pd.read_parquet(file_path)
            df.to_csv(output_file, index=False)
            messagebox.showinfo("Success", f"Converted: {output_file}")
        else:
            messagebox.showerror("Error", "Unsupported file format")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

def convert_folder():
    """Folder selection and batch conversion of CSV ↔ Parquet."""
    folder_path = filedialog.askdirectory(title="Select a Folder Containing CSV or Parquet Files")

    if not folder_path:
        return 

    converted_files = []
    csv, parquet = 0, 0
    try:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                csv_path = os.path.join(CSV_FOLDER, file_name)
                parquet_path = os.path.join(PARQUET_FOLDER, file_name.replace(".csv", ".parquet"))
                try:
                    df = pd.read_csv(csv_path)
                    df.to_parquet(parquet_path, index=False)
                    converted_files.append(parquet_path)
                    csv+=1
                    # print(f"Converted {file_name} → {os.path.basename(parquet_path)}")
                except Exception as e:
                    print(f"Error converting {file_name}: {e}")


            elif file_name.endswith(".parquet"):
                parquet_path = os.path.join(PARQUET_FOLDER, file_name)
                csv_path = os.path.join(CSV_FOLDER, file_name.replace(".parquet", ".csv"))
                try:
                    df = pd.read_parquet(parquet_path)
                    df.to_csv(csv_path, index=False)
                    converted_files.append(csv_path)
                    parquet+=1
                    # print(f"Converted {file_name} → {os.path.basename(csv_path)}")

                except Exception as e:
                    print(f"Error converting {file_name}: {e}")
                    

        if converted_files:
            messagebox.showinfo("Success", f"Converted {csv} .csv files and {parquet} .parquet files.")
        else:
            messagebox.showwarning("No Files Found", "No CSV or Parquet files were found in the folder.")

    except Exception as e:
        messagebox.showerror("Error", f"Batch conversion failed: {e}")

# GUI
root = tk.Tk()
root.title("CSV ↔ Parquet Converter")
root.geometry("400x250")

label = tk.Label(root, text="Select a file or folder to convert", font=("Arial", 12))
label.pack(pady=20)

btn_file = tk.Button(root, text="Select File & Convert", command=convert_file, font=("Arial", 12), bg="lightblue")
btn_file.pack(pady=10)

btn_folder = tk.Button(root, text="Select Folder & Convert All", command=convert_folder, font=("Arial", 12), bg="lightgreen")
btn_folder.pack(pady=10)

root.mainloop()
