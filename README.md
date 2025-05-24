# InsightAI – Role-Aware AI Teammate for Codebase Insights

## Project Overview

InsightAI is an intelligent system that analyzes codebases to extract role-specific insights for different team members. Whether you're a Project Manager, Frontend Developer, Backend Developer, or AI/ML Engineer, InsightAI provides tailored information relevant to your role, helping you quickly understand complex projects.

## System Architecture

```
                                  +----------------+
                                  |                |
                          +-------+    Frontend    +-------+
                          |       |     (React)    |       |
                          |       +----------------+       |
                          |                                |
                          v                                v
                 +----------------+                +----------------+
                 |                |                |                |
                 |   File Upload  |                | Role Selection |
                 |                |                |                |
                 +-------+--------+                +--------+-------+
                         |                                  |
                         v                                  v
                 +-------+----------------------------------+-------+
                 |                                                  |
                 |                   Backend (FastAPI)              |
                 |                                                  |
                 +------+-------------------+--------------------+--+
                        |                   |                    |
                        v                   v                    v
               +--------+-------+  +--------+--------+  +--------+--------+
               |                |  |                 |  |                 |
               |  File Parsing  |  |  RAG Pipeline   |  | Role Templates  |
               |  (Tree-sitter) |  |   (LangChain)   |  |                 |
               |                |  |                 |  |                 |
               +----------------+  +-----------------+  +-----------------+
```

### Key Components:

1. **Frontend**: React application with Tailwind CSS for styling. Provides UI for codebase upload, role selection, and displaying insights.

2. **Backend**: FastAPI server handling file uploads, codebase cloning, and coordinating between parsing and RAG components.

3. **Parsers**: Tree-sitter based code analyzers to extract AST (Abstract Syntax Tree) and detect technologies used in the codebase.

4. **RAG Layer**: LangChain pipelines for Retrieval-Augmented Generation, using vector databases (FAISS) to enhance AI responses with code context.

5. **Role Templates**: Specialized prompt templates designed for different roles (PM, Frontend Dev, Backend Dev, AI/ML Engineer).

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/insightAI.git
cd insightAI

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
cd backend
uvicorn main:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install  # or: yarn install

# Start development server
npm start  # or: yarn start
```

## API Usage Examples

### Upload a Codebase

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/codebase.zip"
```

### Clone a GitHub Repository

```bash
curl -X POST "http://localhost:8000/api/clone" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/username/repository"}'
```

### Get Role-Based Insights

```bash
curl -X POST "http://localhost:8000/api/insights" \
  -H "Content-Type: application/json" \
  -d '{"codebase_id": "abc123", "role": "frontend_developer"}'
```

## Development Guide

### Adding New Roles

To add a new role template:

1. Create a new template file in `/rag/templates/`
2. Register the role in `/rag/role_manager.py`
3. Update the frontend role selector options

### Adding New Parsers

To support a new programming language:

1. Add appropriate Tree-sitter grammar in `/parsers/grammars/`
2. Create a parser implementation in `/parsers/languages/`
3. Register the parser in `/parsers/parser_registry.py`

## Extending the System

### Adding New Visualizations

Add new visualization components in `/frontend/src/components/visualizations/` and update the InsightDisplay component to render them based on the insight type.

### Custom Analysis Plugins

The system supports custom analysis plugins. Create a new plugin in `/parsers/plugins/` and register it in the plugin manager.

## Future Enhancements (Stretch Goals)

- **Agent-to-Agent Communication**: Enable collaboration between multiple AI agents to provide more comprehensive insights
- **Voice Interface**: Add voice input/output capabilities for hands-free interaction
- **Integration with Development Tools**: Connect with Slack, Jira, GitHub to provide insights within existing workflows
- **Real-time Collaboration**: Enable multiple team members to view and discuss insights simultaneously
- **Customizable Role Templates**: Allow users to create and share custom templates for specialized roles