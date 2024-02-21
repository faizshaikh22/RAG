# RAG Application using Gemini-Pro

This project is a RAG (Retrieval-Augmented Generation) application developed using Python, Flask, Langchain, ChromaDB, and Angular. It consists of two microservices:

1. **File Upload**: This microservice is responsible for handling the upload of files to the application. The following file formats are supported:
   - txt
   - pdf
   - docx, doc
   - xlxs, xls
   - pptx

2. **Chat**: This microservice handles the chat functionality of the application, enabling users to chat with each other and share files. The application also stores session logs in a text file located in the folder.
