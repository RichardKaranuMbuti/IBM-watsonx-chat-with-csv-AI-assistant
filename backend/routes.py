from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi import Form,File  # Add this import
from sqlalchemy.orm import Session
from typing import List
import shutil
from . import crud, schemas, models
from .database import get_db
import json
from ai_service.service import process_datasets
from .crud import delete_file

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import os
from starlette import status
import uuid

app = FastAPI()
router = APIRouter()



# Configure Jinja2 templates directory
templates = Jinja2Templates(directory="backend/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("shome.html", {"request": request})

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/upload", response_model=schemas.File)
def upload_file(
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Ensure media directory exists
        os.makedirs("media", exist_ok=True)
        
        # Generate unique filename if needed
        file_path = f"media/{file.filename}"
        
        # Save file directly
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Create file record in database
        return crud.create_file(db, filename=file_path, description=description)
    except Exception as e:
        # More descriptive error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"error": "File upload failed", "message": str(e)}
        )
    
    
@router.get("/files", response_model=List[schemas.File])
def get_all_files(db: Session = Depends(get_db)):
    return crud.get_all_files(db)

@router.get("/file-paths", response_model=List[str])
def get_file_paths(ids: List[int] = None, db: Session = Depends(get_db)):
    return crud.get_file_paths(db, ids=ids)


@router.post("/process-query")
async def process_query(
    request: schemas.QueryRequest,
    db: Session = Depends(get_db)
):
    # Fetch file paths from the database using provided IDs or fetch all if no IDs are given
    file_paths = crud.get_file_paths(db, ids=request.ids)
    if not file_paths:
        raise HTTPException(status_code=404, detail="No files found for the given IDs.")
    
    # Call the process_datasets function with file paths and the query
    result_json = process_datasets(datasets=file_paths, query=request.query)
    
    # Parse the result as a Python dictionary to return
    try:
        result = json.loads(result_json)
        print(f"results : {result}")
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse processing results"
        )

@router.delete("/files/{file_id}")
def delete_file_route(file_id: int, db: Session = Depends(get_db)):
    media_directory = "media"  # Directory where files are stored
    success = delete_file(db, file_id, media_directory)
    if not success:
        raise HTTPException(status_code=404, detail="File not found.")
    return {"message": "File deleted successfully."}


#Page navigation routes
@router.get("/upload-page", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router.get("/files-page", response_class=HTMLResponse)
async def files_page(request: Request):
    return templates.TemplateResponse("manage_files.html", {"request": request})

@router.get("/chat-page", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})