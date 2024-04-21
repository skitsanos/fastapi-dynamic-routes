from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
import shutil

from utils.system import BASE_DIR


async def handler(project_id: str, file: UploadFile = File()):
    # Directory where files will be stored
    upload_folder = f"{BASE_DIR}/uploads/{project_id}/"
    Path(upload_folder).mkdir(parents=True, exist_ok=True)

    file_path = Path(upload_folder) / file.filename

    try:
        # Open the destination file
        with file_path.open("wb") as buffer:
            # Read the file in chunks and write to the destination file
            while True:
                chunk = await file.read(1024 * 1024)  # Read 1MB chunks
                if not chunk:
                    break
                buffer.write(chunk)
    finally:
        # Close the file to free up system resources
        await file.close()

    return {"message": f"Successfully uploaded {file.filename} to project {project_id}."}

# Ensure you integrate this router in your main FastAPI app where routers are included.
