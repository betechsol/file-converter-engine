from fastapi import APIRouter, UploadFile, HTTPException
from ..core.converter import FileConverter
import os
import uuid

router = APIRouter()

@router.post("/convert")
async def convert_file(file: UploadFile):
    valid_extensions = {'.pdf', '.docx', '.png', '.jpg', '.jpeg'}
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in valid_extensions:
        raise HTTPException(400, detail="Unsupported file type")
    
    # Save uploaded file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{uuid.uuid4()}{ext}"
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Convert to text
    output_path = f"{file_path}.txt"
    if ext == '.pdf':
        FileConverter.pdf_to_txt(file_path, output_path)
    elif ext == '.docx':
        FileConverter.docx_to_txt(file_path, output_path)
    else:
        FileConverter.image_to_txt(file_path, output_path)
    
    return {"download_link": f"/api/download/{os.path.basename(output_path)}"}

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(404, detail="File not found")
    return FileResponse(file_path, filename=filename)
