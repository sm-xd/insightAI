"""
RAG pipeline implementation for code analysis.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types import model_types
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

class RagPipeline:
    def __init__(self, config):
        self.config = config
        self.vector_store = None
        self.chain = None
        
    async def initialize(self):
        """Initialize the RAG pipeline components."""
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        
        if not self.vector_store:            self.vector_store = FAISS.load_local(
                self.config.vector_db_path, 
                GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            )
            
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.vector_store.as_retriever(),
            return_source_documents=True
        )
        
    async def process_query(self, query: str, chat_history=None):
        """
        Process a query using the RAG pipeline.
        
        Args:
            query: The user's question
            chat_history: Optional chat history for context
            
        Returns:
            Response from the LLM with relevant context
        """
        if not self.chain:
            await self.initialize()
            
        chat_history = chat_history or []
        response = await self.chain.acall({
            "question": query,
            "chat_history": chat_history
        })
        
        return {
            "answer": response["answer"],
            "sources": [doc.page_content for doc in response["source_documents"]]
        }