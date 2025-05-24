"""
RAG (Retrieval-Augmented Generation) Pipeline for InsightAI.

This module implements the core RAG functionality using LangChain,
combining retrieved context with role-specific prompts.
"""

import os
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from parsers.parser_registry import get_parser_for_file

class RagPipeline:
    """
    RAG Pipeline for generating codebase insights.
    """
    
    def __init__(self, vector_db_path: Optional[str] = None):
        """
        Initialize the RAG pipeline.
        
        Args:
            vector_db_path: Optional path to store vector DB
        """
        self.vector_db_path = vector_db_path or os.getenv("VECTOR_DB_PATH", "./vector_db")
        self._init_components()
      def _init_components(self):
        """Initialize pipeline components."""
        # Initialize Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Initialize embeddings model using HuggingFace (free alternative)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Initialize language model (Gemini Pro)
        self.llm = genai.GenerativeModel('gemini-pro')
        
        # Initialize text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
    
    def index_codebase(self, codebase_path: str, codebase_id: str) -> Any:
        """
        Index a codebase into the vector store.
        
        Args:
            codebase_path: Path to codebase directory
            codebase_id: Unique identifier for the codebase
            
        Returns:
            Vector store instance
        """
        documents = []
        
        # Walk through codebase directory
        for root, _, files in os.walk(codebase_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Get appropriate parser for file
                parser = get_parser_for_file(file_path)
                if parser:
                    try:
                        # Parse file content
                        parsed = parser.parse(file_path)
                        
                        # Create document chunks from parsed content
                        chunks = self.text_splitter.split_text(parsed.raw_content)
                        
                        # Add metadata to chunks
                        for chunk in chunks:
                            documents.append(
                                Document(
                                    page_content=chunk,
                                    metadata={
                                        "file_path": file_path,
                                        "language": parsed.language,
                                        "codebase_id": codebase_id
                                    }
                                )
                            )
                    except Exception as e:
                        print(f"Error parsing {file_path}: {str(e)}")
        
        # Create or load vector store
        store_path = os.path.join(self.vector_db_path, codebase_id)
        
        if os.path.exists(store_path):
            vector_store = FAISS.load_local(store_path, self.embeddings)
            vector_store.add_documents(documents)
        else:
            vector_store = FAISS.from_documents(documents, self.embeddings)
            os.makedirs(store_path, exist_ok=True)
            vector_store.save_local(store_path)
        
        return vector_store
    
    def generate_insights(
        self,
        codebase_path: str,
        role_template: Dict[str, Any],
        specific_focus: Optional[str] = None
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
        """
        Generate role-specific insights for a codebase.
        
        Args:
            codebase_path: Path to codebase directory
            role_template: Role-specific template
            specific_focus: Optional specific area to focus on
            
        Returns:
            Tuple of (insights, visualizations, summary)
        """
        # Index or load codebase
        vector_store = self.index_codebase(
            codebase_path,
            Path(codebase_path).name
        )
        
        # Create retriever
        retriever = vector_store.as_retriever(
            search_type="mmr",  # Maximum Marginal Relevance
            search_kwargs={"k": 5}
        )
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        # Generate insights based on template
        insights = {}
        visualizations = []
        all_responses = []
        
        # Process each analysis task
        for task in role_template["analysis_tasks"]:
            # Build prompt
            prompt = role_template["prompt_template"].format(
                task=task["description"],
                focus=specific_focus or "the entire codebase"
            )
            
            # Get response
            response = qa_chain({"query": prompt})
            all_responses.append(response["result"])
            
            # Process response
            insights[task["id"]] = {
                "question": task["description"],
                "answer": response["result"],
                "task_type": task["type"]
            }
            
            # Generate visualization if specified
            if "visualization" in task:
                visualizations.append({
                    "type": task["visualization"]["type"],
                    "data": response["result"],  # Use response as viz data
                    "config": task["visualization"].get("config", {}),
                    "task_id": task["id"]
                })
        
        # Generate overall summary
        summary_prompt = f"""
        Based on the following insights about the codebase, provide a concise summary
        from the perspective of a {role_template['id']}:
        
        {' '.join(all_responses)}
        """
        
        summary_response = qa_chain({"query": summary_prompt})
        summary = summary_response["result"]
        
        return insights, visualizations, summary