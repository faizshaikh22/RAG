import PyPDF2
import docx
import pandas
from dotenv import load_dotenv
from docx import Document as DocxDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, UnstructuredExcelLoader, Docx2txtLoader, UnstructuredFileLoader, PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader, csv_loader
from langchain.docstore.document import Document

load_dotenv()

class FileConverter:
    def convert_pdf_to_txt(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()
    
        return text

    def convert_docx_to_txt(self, file_path):
        doc = docx.Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        
        return text

    def convert_plain_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        return text

    def convert_excel_to_txt(self, file_path):
        df = pandas.read_excel(file_path)
        return df.to_string()

    # def convert_to_text(self, file_path, file_type):
    #     if file_type == 'PDF':
    #         return self.convert_pdf_to_txt(file_path)
    #     elif file_type == 'DOCX':
    #         return self.convert_docx_to_txt(file_path)
    #     elif file_type == 'Excel':
    #         return self.convert_excel_to_txt(file_path)
    #     elif file_type == 'Text':
    #         return self.convert_plain_txt(file_path)
    #     else:
    #         return "Error: Unsupported file type"
    
    def convert_to_document(self, file_path, file_type):
        document = []
        if file_type == 'PDF':
            loader = PyPDFLoader(file_path)
            document.extend(loader.load())
            return document
        elif file_type == 'DOCX':
            loader = Docx2txtLoader(file_path)
            document.extend(loader.load())
            return document
        elif file_type == 'Excel':
            loader = UnstructuredExcelLoader(file_path)
            document.extend(loader.load())
            return document
        elif file_type == 'Text':
            loader = TextLoader(file_path)
            document.extend(loader.load())
            return document
        elif file_type == 'PPTX':
            loader = UnstructuredPowerPointLoader(file_path)
            document.extend(loader.load())
            return document
        # elif file_type == 'PPT':
        #     loader = UnstructuredPowerPointLoader(file_path)
        #     document.extend(loader.load())
        #     return document
        elif file_type == 'CSV':
            loader = csv_loader.CSVLoader(file_path, csv_args={
                "delimiter": ",",
                "quotechar": '"',
            })
            document.extend(loader.load())
            return document
        else:
            return "Error: Unsupported file type"

class Helpers:
    def __init__(self):
        self.file_converter = FileConverter()

    def convert_to_chunks(self, file_path, file_type):
        document = self.file_converter.convert_to_document(file_path, file_type)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len,
            add_start_index = True
        )
        
        chunks = text_splitter.split_documents(document)
        print(f"Split {document} documents into {len(chunks)} chunks.")
        
        return chunks
