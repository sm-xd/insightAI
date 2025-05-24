"""
Tests for the RAG pipeline.
"""

import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from pathlib import Path
import json

from rag.pipeline import RagPipeline
from rag.role_manager import RoleManager


class TestRagPipeline(unittest.TestCase):
    """Test cases for the RAG pipeline."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temp directories
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vector_db_path = os.path.join(self.temp_dir.name, "vector_db")
        os.makedirs(self.vector_db_path, exist_ok=True)
        
        # Create a sample codebase directory
        self.codebase_path = os.path.join(self.temp_dir.name, "sample_codebase")
        os.makedirs(self.codebase_path, exist_ok=True)
        
        # Create a sample Python file
        py_content = """
import os
import sys

def hello_world():
    \"\"\"Say hello to the world.\"\"\"
    print("Hello, World!")
    
class Calculator:
    \"\"\"A simple calculator class.\"\"\"
    
    def __init__(self):
        self.value = 0
        
    def add(self, x):
        \"\"\"Add a number to the current value.\"\"\"
        self.value += x
        return self.value
"""
        with open(os.path.join(self.codebase_path, "calculator.py"), 'w') as f:
            f.write(py_content)
        
        # Create a sample JavaScript file
        js_content = """
import { Component } from 'react';
const axios = require('axios');

// Constants
const API_URL = 'https://api.example.com';

class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl || API_URL;
  }
  
  async fetchData(endpoint) {
    try {
      const response = await axios.get(`${this.baseUrl}/${endpoint}`);
      return response.data;
    } catch (error) {
      console.error('API error:', error);
      return null;
    }
  }
}

export default new ApiClient();
"""
        with open(os.path.join(self.codebase_path, "api_client.js"), 'w') as f:
            f.write(js_content)
    
    def tearDown(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()
    
    @patch('rag.pipeline.OpenAIEmbeddings')
    @patch('rag.pipeline.FAISS')
    @patch('rag.pipeline.OpenAI')
    @patch('rag.pipeline.RetrievalQA')
    def test_index_codebase(self, mock_retrieval_qa, mock_openai, mock_faiss, mock_embeddings):
        """Test indexing a codebase."""
        # Setup mocks
        mock_vector_store = MagicMock()
        mock_faiss.from_documents.return_value = mock_vector_store
        
        # Create pipeline with mock vector DB path
        pipeline = RagPipeline(vector_db_path=self.vector_db_path)
        
        # Index the codebase
        codebase_id = "test-codebase"
        result = pipeline.index_codebase(self.codebase_path, codebase_id)
        
        # Check that the vector store was created
        self.assertEqual(result, mock_vector_store)
        mock_faiss.from_documents.assert_called_once()
    
    @patch('rag.pipeline.OpenAIEmbeddings')
    @patch('rag.pipeline.FAISS')
    @patch('rag.pipeline.OpenAI')
    @patch('rag.pipeline.RetrievalQA')
    def test_generate_insights(self, mock_retrieval_qa, mock_openai, mock_faiss, mock_embeddings):
        """Test generating insights with a role template."""
        # Setup mocks
        mock_vector_store = MagicMock()
        mock_retriever = MagicMock()
        mock_vector_store.as_retriever.return_value = mock_retriever
        mock_faiss.from_documents.return_value = mock_vector_store
        
        # Setup QA chain mock
        mock_qa_chain = MagicMock()
        mock_qa_chain.return_value = {"result": "Test insight"}
        mock_retrieval_qa.from_chain_type.return_value = mock_qa_chain
        
        # Create pipeline with mock vector DB path
        pipeline = RagPipeline(vector_db_path=self.vector_db_path)
        
        # Get a role template
        role_manager = RoleManager()
        template = role_manager.get_template("project_manager")
        
        # Generate insights (this will use the mocked QA chain)
        insights, visualizations, summary = pipeline.generate_insights(
            codebase_path=self.codebase_path,
            role_template=template
        )
        
        # Check the results
        self.assertIsInstance(insights, dict)
        self.assertIsInstance(visualizations, list)
        self.assertEqual(summary, "Test insight")


class TestRoleManager(unittest.TestCase):
    """Test cases for the Role Manager."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temp directory for templates
        self.temp_dir = tempfile.mkdtemp()
        self.role_manager = RoleManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_default_templates(self):
        """Test default templates are created."""
        # Default roles should be available
        roles = self.role_manager.get_available_roles()
        role_ids = [role["id"] for role in roles]
        
        self.assertIn("project_manager", role_ids)
        self.assertIn("frontend_developer", role_ids)
        self.assertIn("backend_developer", role_ids)
        self.assertIn("ai_ml_engineer", role_ids)
    
    def test_get_template(self):
        """Test retrieving a template."""
        template = self.role_manager.get_template("project_manager")
        
        self.assertEqual(template["id"], "project_manager")
        self.assertIn("prompt_template", template)
        self.assertIn("analysis_tasks", template)
    
    def test_add_template(self):
        """Test adding a new template."""
        new_template = {
            "id": "devops_engineer",
            "name": "DevOps Engineer",
            "description": "Focus on infrastructure and deployment",
            "prompt_template": "As a DevOps Engineer, analyze {focus} and provide insights about {task}.",
            "analysis_tasks": [
                {
                    "id": "infrastructure",
                    "type": "infrastructure",
                    "description": "What infrastructure components are used?"
                }
            ]
        }
        
        self.role_manager.add_template(new_template)
        template = self.role_manager.get_template("devops_engineer")
        
        self.assertEqual(template["id"], "devops_engineer")
        self.assertEqual(template["name"], "DevOps Engineer")
    
    def test_remove_template(self):
        """Test removing a template."""
        # First add a template
        new_template = {
            "id": "test_role",
            "name": "Test Role",
            "description": "Test template",
            "prompt_template": "Test prompt {focus} {task}",
            "analysis_tasks": []
        }
        self.role_manager.add_template(new_template)
        
        # Then remove it
        self.role_manager.remove_template("test_role")
        
        # Check that it's gone
        with self.assertRaises(ValueError):
            self.role_manager.get_template("test_role")
    
    def test_invalid_template(self):
        """Test handling invalid templates."""
        invalid_template = {
            "id": "invalid",
            "name": "Invalid Template"
            # Missing required fields
        }
        
        with self.assertRaises(ValueError):
            self.role_manager.add_template(invalid_template)
    
    def test_template_file_persistence(self):
        """Test that templates are saved to files."""
        new_template = {
            "id": "persistent_role",
            "name": "Persistent Role",
            "description": "Test persistence",
            "prompt_template": "Test prompt {focus} {task}",
            "analysis_tasks": []
        }
        
        # Add template
        self.role_manager.add_template(new_template)
        
        # Check that file exists
        template_path = Path(self.temp_dir) / "persistent_role.json"
        self.assertTrue(template_path.exists())
        
        # Check file content
        with open(template_path) as f:
            saved_template = json.load(f)
        
        self.assertEqual(saved_template["id"], "persistent_role")
        self.assertEqual(saved_template["name"], "Persistent Role")

if __name__ == '__main__':
    unittest.main()