from pdf2docx import Converter
import win32com.client
import os


os.makedirs("pdf", exist_ok=True)
os.makedirs("word", exist_ok=True)
os.makedirs("input", exist_ok=True)
def pdf_to_word(pdf_path, word_path):
    """Convert PDF to Word"""
    try:
        pdf_path = os.path.abspath(pdf_path)
        word_path = os.path.abspath(word_path)
        
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()
        print(f"✅ Converted '{pdf_path}' to '{word_path}'")
    
    except Exception as e:
        print(f"❌ PDF to Word conversion failed: {e}")

def word_to_pdf(word_path, pdf_path):
    """Convert Word to PDF"""
    try:
        word_path = os.path.abspath(word_path)
        pdf_path = os.path.abspath(pdf_path)

        if not os.path.exists(word_path):
            print(f"Error: The file '{word_path}' does not exist.")
            return
        
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False 
        doc = word.Documents.Open(word_path)

        if doc is None:
            print(f"Error: Failed to open document '{word_path}'.")
            word.Quit()
            return
        
        doc.SaveAs(pdf_path, FileFormat=17)
        doc.Close()
        word.Quit()
        
        print(f"✅ Converted '{word_path}' to '{pdf_path}'")

    except Exception as e:
        print(f"❌ Word to PDF conversion failed: {e}")
        word.Quit()

def auto_convert(directory):
    """Automatically convert all PDFs to Word and all Word documents to PDFs in the input folder"""
    directory = os.path.abspath(directory)  
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        if file.endswith(".pdf"):
            word_path = os.path.join("word", file.replace(".pdf", ".docx"))
            pdf_to_word(file_path, word_path)

        elif file.endswith(".docx"):
            pdf_path = os.path.join("pdf", file.replace(".docx", ".pdf"))
            word_to_pdf(file_path, pdf_path)

if __name__ == "__main__":
    auto_convert("input")

