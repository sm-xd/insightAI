"""
Main FastAPI application for InsightAI.
"""

import os
import shutil
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from pydantic import BaseModel

from rag.pipeline import RagPipeline
from rag.role_manager import RoleManager
from parsers.parser_registry import get_parser_for_file

# Create FastAPI app
app = FastAPI(
    title="InsightAI API",
    description="Role-aware AI teammate for codebase insights",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
role_manager = RoleManager()
rag_pipeline = RagPipeline(settings)

# Store active codebases
codebases: Dict[str, Dict[str, Any]] = {}

# Models
class CloneRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"

class InsightRequest(BaseModel):
    codebase_id: str
    role: str
    specific_focus: Optional[str] = None

@app.get("/")
async def serverstatus() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "running"}

@app.post("/api/upload")
async def upload_codebase(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a codebase ZIP file for analysis.
    """
    if not file.filename.endswith(('.zip', '.tar.gz', '.tgz')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a ZIP or tar.gz file."
        )
    
    try:
        # Create unique codebase ID and temp directory
        codebase_id = str(uuid.uuid4())
        temp_dir = Path(tempfile.mkdtemp())
        upload_path = temp_dir / file.filename
        
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract archive
        extract_dir = temp_dir / "extracted"
        extract_dir.mkdir()
        
        if file.filename.endswith('.zip'):
            shutil.unpack_archive(upload_path, extract_dir, 'zip')
        else:
            shutil.unpack_archive(upload_path, extract_dir, 'gztar')
        
        # Store codebase info
        codebases[codebase_id] = {
            "id": codebase_id,
            "name": file.filename,
            "path": str(extract_dir),
            "status": "ready"
        }
        
        return {
            "codebase_id": codebase_id,
            "message": "Codebase uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing upload: {str(e)}"
        )
    
    finally:
        await file.close()

@app.post("/api/clone")
async def clone_repository(request: CloneRequest) -> Dict[str, Any]:
    """
    Clone a GitHub repository for analysis.
    """
    try:
        # Create unique codebase ID and temp directory
        codebase_id = str(uuid.uuid4())
        temp_dir = Path(tempfile.mkdtemp())
        
        # TODO: Implement actual git clone
        # For now, return placeholder response
        codebases[codebase_id] = {
            "id": codebase_id,
            "name": request.repo_url.split("/")[-1],
            "path": str(temp_dir),
            "status": "pending",
            "repo_url": request.repo_url,
            "branch": request.branch
        }
        
        return {
            "codebase_id": codebase_id,
            "message": "Repository clone initiated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error cloning repository: {str(e)}"
        )

@app.post("/api/insights")
async def get_insights(request: InsightRequest) -> Dict[str, Any]:
    """
    Get role-based insights for a codebase.
    """
    if request.codebase_id not in codebases:
        raise HTTPException(
            status_code=404,
            detail="Codebase not found"
        )
    
    codebase = codebases[request.codebase_id]
    if codebase["status"] != "ready":
        raise HTTPException(
            status_code=400,
            detail="Codebase is not ready for analysis"
        )
    
    try:
        # Get role template
        template = role_manager.get_template(request.role)
        
        # Generate insights
        insights, visualizations, summary = rag_pipeline.generate_insights(
            codebase_path=codebase["path"],
            role_template=template,
            specific_focus=request.specific_focus
        )
        
        return {
            "insights": insights,
            "visualizations": visualizations,
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating insights: {str(e)}"
        )

@app.get("/api/roles")
async def get_roles() -> Dict[str, Any]:
    """
    Get available role templates.
    """
    roles = role_manager.get_available_roles()
    return {"roles": roles}

@app.get("/api/status/{codebase_id}")
async def get_status(codebase_id: str) -> Dict[str, Any]:
    """
    Get codebase processing status.
    """
    if codebase_id not in codebases:
        raise HTTPException(
            status_code=404,
            detail="Codebase not found"
        )
    
    return {
        "status": codebases[codebase_id]["status"],
        "message": "Status retrieved successfully"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)