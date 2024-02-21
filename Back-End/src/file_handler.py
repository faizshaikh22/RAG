import mimetypes
import os
from dotenv import load_dotenv
import logging
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from helpers import Helpers
from db import DataBase

load_dotenv()

fileController = Blueprint("upload", __name__)

class FileHandler:
    UPLOAD_FOLDER = "../uploads"

    def __init__(self, app):
        self.app = app
        CORS(self.app, resources={r"/upload": {"origins": "*"}})
        self.helper = Helpers()
        self.db = DataBase()
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/upload', methods=['POST'])(self.upload_file)

    @staticmethod
    def check_file_type(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if file_path.lower().endswith('.pdf'):
            return "PDF"
        elif file_path.lower().endswith('.xls') or file_path.lower().endswith('.xlsx'):
            return "Excel"
        elif file_path.lower().endswith('.pptx'):
            return "PPTX"
        # elif file_path.lower().endswith('.ppt'):
        #     return "PPT"
        elif file_path.lower().endswith('.txt'):
            return "Text"
        elif file_path.lower().endswith('.docx'):
            return "DOCX"
        elif file_path.lower().endswith('.csv'):
            return "CSV"
        
        return "Error: Unsupported filetype"

        # if mime_type:
        #     if "pdf" in mime_type.lower():
        #         return "PDF"
        #     elif "vnd.openxmlformats-officedocument.wordprocessingml.document" in mime_type.lower():
        #         return "DOCX"
        #     elif "text/csv" in mime_type.lower():
        #         print("csv")
        #         return "CSV"
        #     elif "excel" in mime_type.lower() or "vnd.openxmlformats-officedocument.spreadsheetml.sheet" in mime_type.lower():
        #         return "Excel"
        #     elif "text" in mime_type.lower():
        #         return "Text"
        #     elif "vnd.openxmlformats-officedocument.presentationml.presentation" in mime_type.lower():
        #         return "PPTX"
        #     # elif "ppt" in mime_type.lower() or file_path.lower().endswith('.ppt') or "vnd.ms-powerpoint" in mime_type.lower():
        #     #     return "PPT"
        # return "Error: Unsupported file type"

    @staticmethod
    def file_exists_in_dir(filename, folder):
        file_path = os.path.join(folder, filename)
        return os.path.exists(file_path)

    @staticmethod
    def save_file(file, file_path):
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @fileController.route('/upload', methods=['POST'])
    def upload_file():
        try:
            if 'file' not in request.files:
                logging.info("No file provided.")
                return jsonify({"error": "No file provided"}), 400

            file = request.files['file']

            if file.filename == '':
                logging.info("No file selected.")
                return jsonify({"error": "No file selected"}), 400

            file_type = FileHandler.check_file_type(file.filename)

            if "Error" in file_type:
                logging.error(f"Unsupported file type: {file_type}")
                return jsonify({"error": file_type}), 400

            file_path = os.path.join(FileHandler.UPLOAD_FOLDER, file.filename)

            if FileHandler.file_exists_in_dir(file.filename, FileHandler.UPLOAD_FOLDER):
                logging.warning(f"File already exists: {file.filename}")
                return jsonify({"error": "File already exists"}), 400

            FileHandler.save_file(file, file_path)
            logging.info(f"File uploaded successfully: {file.filename}")

            helper = Helpers()
            texts = helper.convert_to_chunks(file_path, file_type)
            logging.info(f"Converted file to chunks: {file.filename}")
            print(texts[0])

            db = DataBase()
            db.save_to_chroma(texts)

            return jsonify({"success": f"File type: {file_type}"}), 200
        except Exception as e:
            logging.exception("An error occurred during file upload.")
            return jsonify({"error": str(e)}), 500

    # def run(self):
    #     self.app.run(debug=True)

app = Flask(__name__)
file_handler = FileHandler(app)

if __name__ == '__main__':
    os.makedirs(FileHandler.UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
