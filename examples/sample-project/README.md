# Sample Project

This is a simple React/Node.js project to test InsightAI's analysis capabilities.

## Structure

```
sample-project/
├── frontend/        # React frontend
│   ├── src/
│   └── package.json
└── backend/         # Node.js backend
    ├── src/
    └── package.json
```

## Usage

1. Zip this directory:
   ```bash
   zip -r sample-project.zip .
   ```

2. Upload to InsightAI:
   ```bash
   curl -X POST "http://localhost:8000/api/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample-project.zip"
   ```

3. Try different roles to see various insights