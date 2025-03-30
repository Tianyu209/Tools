# File Format Converter

A Flask web application that converts between different file formats:
- PDF to Word (DOCX)
- Word (DOCX) to PDF
- CSV to Parquet
- Parquet to CSV

## Docker Setup

### Build the Docker Image

```bash
docker build -t file-converter .
```

### Run the Container

```bash
docker run -p 5000:5000 file-converter
```

The application will be available at http://localhost:5000

## Features

- Simple web interface for file uploads
- Automatic file format detection
- Supports multiple file format conversions
- Automatic cleanup of temporary files

## Note

The application creates necessary directories (uploads, pdf, word) automatically and handles file cleanup after conversion.