# Getting Started with InsightAI

## Prerequisites Installation

1. Install Python 3.9+ from [python.org](https://python.org)
2. Install Node.js 16+ from [nodejs.org](https://nodejs.org)
3. Install Git from [git-scm.com](https://git-scm.com)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/insightAI.git
cd insightAI
```

### 2. Backend Setup

#### Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Install dependencies:
```bash
# Windows
python -m pip install --upgrade pip  # Update pip first
pip install -r requirements.txt
pip install python-dotenv  # Ensure dotenv is installed
pip install -e .  # Install package in development mode

# macOS/Linux
python3 -m pip install --upgrade pip  # Update pip first
pip3 install -r requirements.txt
pip3 install python-dotenv  # Ensure dotenv is installed
pip3 install -e .  # Install package in development mode
```

#### Configure environment:
Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here  # Get from https://makersuite.google.com/app/apikey
DEBUG=True
HOST=0.0.0.0
PORT=8000
VECTOR_DB_PATH=./vector_db
```

#### Start backend server:
```bash
# Make sure you're in the backend directory
cd backend

# Start the server
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### 3. Frontend Setup

In a new terminal:
```bash
# Navigate to frontend directory
cd frontend

# Create .env file with API configuration
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Install dependencies (run this only once or when dependencies change)
npm install

# Start the development server
npm start

# The frontend will be available at http://localhost:3000
# Wait for the message "Compiled successfully!" before accessing the URL
```

Note: Make sure both the backend and frontend servers are running simultaneously in separate terminals.

## Verify Installation

1. Verify both servers are running:
   - Backend: http://localhost:8000/docs should show the FastAPI docs
   - Frontend: http://localhost:3000 should show the InsightAI interface

2. Test the system:
   - Upload a small test codebase (e.g., a single Python file)
   - Select a role (e.g., "Software Architect")
   - Submit a question about the code
   - Verify that you receive an AI-generated response

3. If the upload fails:
   - Check both terminal windows for error messages
   - Verify your GOOGLE_API_KEY in .env is valid
   - Ensure the backend can write to ./vector_db directory

## Common Issues

### Backend Issues:
- If `uvicorn` fails, check Python version and virtual environment activation
- If API calls fail, verify GOOGLE_API_KEY in .env
- Check backend logs for detailed error messages

### Frontend Issues:
- If npm install fails, delete node_modules and package-lock.json, then retry
- If API calls fail, check REACT_APP_API_URL in frontend/.env
- Enable browser developer tools for error details

## Development Workflow

1. Backend changes:
   ```bash
   uvicorn main:app --reload  # Auto-reloads on changes
   ```

2. Frontend changes:
   ```bash
   npm start  # Auto-reloads on changes
   ```

3. Running tests:
   ```bash
   # Backend tests
   python -m pytest tests/

   # Frontend tests
   cd frontend
   npm test
   ```

## Next Steps

1. Review the main README.md for system architecture
2. Check CONTRIBUTING.md for development guidelines
3. Explore `/examples` directory for usage examples
4. Join our community Discord for support