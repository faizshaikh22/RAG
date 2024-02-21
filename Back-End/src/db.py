import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

class DataBase:
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    chroma_path = "../db"
    
    def save_to_chroma(self, chunks):
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=self.GOOGLE_API_KEY, model="models/embedding-001")
        db = Chroma.from_documents(
            chunks, embeddings, persist_directory=self.chroma_path
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {self.chroma_path}")