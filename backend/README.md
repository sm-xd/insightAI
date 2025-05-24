# Backend Server

FastAPI-based backend server for InsightAI.

## Structure

```
backend/
├── main.py      # FastAPI application and endpoints
├── config.py    # Configuration settings
└── utils.py     # Utility functions
```

## API Endpoints

### File Upload
```http
POST /api/upload
Content-Type: multipart/form-data
file: @codebase.zip

Response: {
  "codebase_id": "uuid",
  "message": "success"
}
```

### Repository Clone
```http
POST /api/clone
Content-Type: application/json
{
  "repo_url": "https://github.com/user/repo",
  "branch": "main"
}

Response: {
  "codebase_id": "uuid",
  "message": "success"
}
```

### Get Insights
```http
POST /api/insights
Content-Type: application/json
{
  "codebase_id": "uuid",
  "role": "role_id",
  "specific_focus": "optional_focus"
}

Response: {
  "insights": {},
  "visualizations": [],
  "summary": "string"
}
```

## Configuration

Environment variables (`.env`):
```bash
DEBUG=True
HOST=0.0.0.0
PORT=8000
WORKERS=4
MAX_UPLOAD_SIZE_MB=100
MAX_TOKENS=4000
REQUEST_TIMEOUT=300
```

## Running the Server

Development:
```bash
uvicorn main:app --reload
```

Production:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

Common error responses:
- 400: Invalid request (e.g., unsupported file type)
- 404: Resource not found
- 413: File too large
- 500: Internal server error

## CORS Configuration

Default allowed origins:
- http://localhost:3000 (React dev server)
- http://localhost:8000 (FastAPI server)