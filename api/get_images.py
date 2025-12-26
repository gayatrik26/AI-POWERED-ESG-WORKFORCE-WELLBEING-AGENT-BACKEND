import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

IMAGE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data_pipeline', 'employee_images')

@router.get("/images/{employee_id}/{image_name}")
async def get_employee_image(employee_id: str, image_name: str):
    image_path = os.path.join(IMAGE_DIR, employee_id, image_name)
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    
    raise HTTPException(status_code=404, detail="Image not found")
