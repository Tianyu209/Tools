from flask import Flask, render_template, request, send_file, jsonify
import os
from pdf2word.auto_convert import pdf_to_word, word_to_pdf
import pandas as pd
import webbrowser
from threading import Timer
import logging
import threading
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.makedirs("uploads", exist_ok=True)
def delayed_file_cleanup(file_path, delay=5):
    """delete files after a delay"""
    def delete_file():
        time.sleep(delay)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f'Cleaned up file (delayed): {file_path}')
        except Exception as e:
            logger.error(f'Failed to clean up file (delayed): {e}')
    
    threading.Thread(target=delete_file).start()
def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
           static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
logger.info(f"Upload folder path: {app.config['UPLOAD_FOLDER']}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    input_path = None
    output_path = None
    
    try:
        if 'file' not in request.files:
            logger.error('No file in request')
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error('Empty filename')
            return jsonify({'error': 'No file selected'}), 400

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            logger.info('Recreating upload folder')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        import re
        safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', file.filename)
        logger.info(f'Processing file: {safe_filename}')
        
        input_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], safe_filename))
        logger.info(f'Saving file to: {input_path}')
        print(input_path)
        file.save(input_path)
        
        if not os.path.exists(input_path):
            logger.error(f'Failed to save file to: {input_path}')
            return jsonify({'error': 'Failed to save uploaded file'}), 500

        logger.info(f'File saved successfully: {input_path}')
        
        filename, ext = os.path.splitext(safe_filename)
        
        try:
            if ext.lower() == '.pdf':
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.docx")
                logger.info(f'Converting PDF to Word: {output_path}')
                pdf_to_word(input_path, output_path)
            elif ext.lower() == '.docx':
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.pdf")
                logger.info(f'Converting Word to PDF: {output_path}')
                word_to_pdf(input_path, output_path)
            elif ext.lower() == '.csv':
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.parquet")
                logger.info(f'Converting CSV to Parquet: {output_path}')
                df = pd.read_csv(input_path)
                df.to_parquet(output_path, index=False)
            elif ext.lower() == '.parquet':
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.csv")
                logger.info(f'Converting Parquet to CSV: {output_path}')
                df = pd.read_parquet(input_path)
                df.to_csv(output_path, index=False)
            else:
                logger.error(f'Unsupported file format: {ext}')
                return jsonify({'error': 'Unsupported file format'}), 400

            logger.info('Sending converted file')
            return_value = send_file(output_path, as_attachment=True)
            
            if input_path and os.path.exists(input_path):
                try:
                    os.remove(input_path)
                    logger.info(f'Cleaned up input file: {input_path}')
                except Exception as e:
                    logger.error(f'Failed to clean up input file: {e}')

            if output_path and os.path.exists(output_path):
                delayed_file_cleanup(output_path)
                logger.info(f'Scheduled delayed cleanup for output file: {output_path}')

            return return_value

        except Exception as e:
            logger.error(f'Conversion failed: {str(e)}')
            if ext.lower() == '.pdf':
                return jsonify({'error': f'PDF转Word失败: {str(e)}。请检查PDF文件是否有效且未损坏。'}), 500
            elif ext.lower() == '.docx':
                return jsonify({'error': f'Word转PDF失败: {str(e)}。请检查Word文件是否有效且未损坏。'}), 500
            elif ext.lower() == '.csv':
                return jsonify({'error': f'CSV转Parquet失败: {str(e)}。请检查CSV文件格式是否正确。'}), 500
            elif ext.lower() == '.parquet':
                return jsonify({'error': f'Parquet转CSV失败: {str(e)}。请检查Parquet文件是否有效。'}), 500
            else:
                return jsonify({'error': f'转换失败: {str(e)}'}), 500
    except Exception as e:
        logger.error(f'Conversion failed: {str(e)}')
        if input_path and os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)