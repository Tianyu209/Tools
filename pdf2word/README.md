# auto_convert.py

This script does the following:

1. **Folder Creation**: If the folders "pdf" and "word" do not exist, they will be created in the same directory as the selected folder.
2. **File Conversion**:
    - Converts all PDF files in the selected folder to Word files in the "word" folder.
    - Converts all Word files in the selected folder to PDF files in the "pdf" folder.

---

# gui.py

This script provides a GUI with two buttons for file and folder conversion:

1. **File Convert**:  
   Converts a single file (either PDF or Word) to the other format.

2. **Folder Convert**:  
   Converts all files in a selected folder (PDF or Word) to the other format:
   - PDF files will be stored in the "pdf" folder.
   - Word files will be stored in the "word" folder.