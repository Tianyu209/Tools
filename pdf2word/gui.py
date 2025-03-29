import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import win32com.client

def pdf_to_word(pdf_path, word_path):
    try:
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()
        messagebox.showinfo("Success", f"Converted: {word_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

def word_to_pdf(word_path, pdf_path):
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(word_path))
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        doc.Close()
        word.Quit()
        messagebox.showinfo("Success", f"Converted: {pdf_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

def convert_file():
    file_path = filedialog.askopenfilename(title="Select a PDF or Word File",
                                           filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
    if not file_path:
        return
    
    file_dir, file_name = os.path.split(file_path)
    if file_path.endswith(".pdf"):
        word_path = os.path.join(file_dir, file_name.replace(".pdf", ".docx"))
        pdf_to_word(file_path, word_path)
    elif file_path.endswith(".docx"):
        pdf_path = os.path.join(file_dir, file_name.replace(".docx", ".pdf"))
        word_to_pdf(file_path, pdf_path)
    else:
        messagebox.showerror("Error", "Unsupported file format")

def convert_folder():
    folder_path = filedialog.askdirectory(title="Select a Folder Containing PDF or Word Files")
    if not folder_path:
        return
    
    pdf_folder = os.path.join(folder_path, "pdf")
    word_folder = os.path.join(folder_path, "word")
    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(word_folder, exist_ok=True)
    
    converted_files = []
    pdf_count, word_count = 0, 0
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".pdf"):
            word_path = os.path.join(word_folder, file_name.replace(".pdf", ".docx"))
            pdf_to_word(file_path, word_path)
            converted_files.append(word_path)
            pdf_count += 1
        elif file_name.endswith(".docx"):
            pdf_path = os.path.join(pdf_folder, file_name.replace(".docx", ".pdf"))
            word_to_pdf(file_path, pdf_path)
            converted_files.append(pdf_path)
            word_count += 1
    
    if converted_files:
        messagebox.showinfo("Success", f"Converted {pdf_count} PDFs and {word_count} Word files.")
    else:
        messagebox.showwarning("No Files Found", "No PDF or Word files were found in the folder.")

# GUI
root = tk.Tk()
root.title("PDF ↔ Word Converter")
root.geometry("400x250")

label = tk.Label(root, text="Select a file or folder to convert", font=("Arial", 12))
label.pack(pady=20)

btn_file = tk.Button(root, text="Select File & Convert", command=convert_file, font=("Arial", 12), bg="lightblue")
btn_file.pack(pady=10)

btn_folder = tk.Button(root, text="Select Folder & Convert All", command=convert_folder, font=("Arial", 12), bg="lightgreen")
btn_folder.pack(pady=10)

root.mainloop()
