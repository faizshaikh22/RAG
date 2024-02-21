import os
import logging
import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain

chatController = Blueprint("chat", __name__)

load_dotenv()

class ChatHandler:
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    CHROMA_PATH = "../db"

    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.route('/chat', methods=['post'])(self.input)
        # chatController.route('/chat', methods=['POST'])(self.input)
        self.setup_logger()

    @staticmethod
    # def response(question):
    #     embeddings = GoogleGenerativeAIEmbeddings(google_api_key=ChatHandler.GOOGLE_API_KEY, model="models/embedding-001")
    #     db = Chroma(persist_directory=ChatHandler.CHROMA_PATH, embedding_function=embeddings)

    #     results = db.similarity_search_with_relevance_scores(question, 2)
    #     if len(results) == 0 or results[0][1] < 0.5:
    #         print(f"Unable to find matching results.")
    #         return "Unable to find matching results"

    #     context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
    #     print(context)

    #     PROMPT_TEMPLATE = """
    #     Answer the question based only on the following context:

    #     {context}

    #     ---

    #     Answer the question based on the above context: {question}
    #     """
        
        
    #     prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    #     prompt = prompt_template.format(context=context, question=question)
        
    #     print(prompt)
        
    #     model = ChatGoogleGenerativeAI(google_api_key=ChatHandler.GOOGLE_API_KEY, model="gemini-pro", temperature=0.3)
        
    #     response_text = model.predict(prompt)

    #     sources = [doc.metadata.get("source", None) for doc, _score in results]
    #     formatted_response = f"Response: {response_text}\nSources: {sources}"
        
    #     print(formatted_response)
        
    #     return response_text
        
        # prompt = PromptTemplate(template = PROMPT_TEMPLATE, input_variables = ["context", "question"])

        # model = ChatGoogleGenerativeAI(google_api_key=ChatHandler.GOOGLE_API_KEY, model="gemini-pro", temperature=0.3)
        # chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        # response = chain(
        #     {"input_documents":response, "question": question}
        #     , return_only_outputs=True
        # )

        # print(response)
        
        # return response

    def response(question):
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=ChatHandler.GOOGLE_API_KEY, model="models/embedding-001")
        db = Chroma(persist_directory=ChatHandler.CHROMA_PATH, embedding_function=embeddings)
            
        results  = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
        
        print(results)
            
        llm = ChatGoogleGenerativeAI(google_api_key=ChatHandler.GOOGLE_API_KEY, model="gemini-pro", temperature=0.3, convert_system_message_to_human=True,
                                     safety_settings={
                                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                    })
            
        qa = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=results, return_source_documents=True)
        
        result = qa({
            "query": question,
        }, return_only_outputs=True)
        
        print(qa({
            "query":question
        }))
        
        # print(result)
    
        return result["result"]

    # @chatController.route('/chat', methods=['POST'])
    def input(self):
        try:
            input_text = request.json['text']
            output_text = self.response(input_text)
            self.log_info(input_text, output_text)
            return jsonify({"output": output_text})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        log_path = f"../logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')} - chat_logs.txt"
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_info(self, input_text, output_text):
        self.logger.info(f"Input: {input_text}")
        self.logger.info(f"Output: {output_text}")

    def run(self):
        self.app.run(port=5001, debug=True)

if __name__ == '__main__':
    chat_handler = ChatHandler()
    chat_handler.run()