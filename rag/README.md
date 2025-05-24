# RAG (Retrieval-Augmented Generation)

This package implements the core RAG functionality using LangChain, combining retrieved context with role-specific prompts.

## Structure

```
rag/
├── templates/    # Role-specific prompt templates
├── pipeline.py   # RAG pipeline implementation
└── role_manager.py # Role template management
```

## Role Templates

Templates are stored in JSON format in `templates/`:

```json
{
  "id": "role_id",
  "name": "Role Name",
  "description": "Role description",
  "prompt_template": "As a {role}, analyze {focus} and provide insights about {task}",
  "analysis_tasks": [
    {
      "id": "task_id",
      "type": "task_type",
      "description": "Task description",
      "visualization": {
        "type": "visualization_type",
        "config": {}
      }
    }
  ]
}
```

## Adding a New Role

1. Create template JSON file in `templates/`
2. Register role in `role_manager.py`:
```python
role_manager.add_template({
    "id": "new_role",
    "name": "New Role",
    # ... template configuration
})
```

## Environment Setup

Required environment variables:
```bash
OPENAI_API_KEY=your_api_key
VECTOR_DB_PATH=path/to/vector/db
```

## Vector Database

- Uses FAISS for efficient similarity search
- Stores embeddings in `VECTOR_DB_PATH`
- Auto-creates per-codebase indexes

## Running Tests

```bash
# From project root
python -m pytest tests/test_rag.py
```

## LangChain Configuration

Default settings:
- Model: GPT-4
- Temperature: 0.7
- Max tokens: 4000
- Retrieval: MMR strategy with k=5

## Customization

- Modify prompt templates in `templates/`
- Adjust model parameters in `pipeline.py`
- Add custom retrievers in `pipeline.py`