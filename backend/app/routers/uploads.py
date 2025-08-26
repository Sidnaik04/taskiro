from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.cloudinary__client import upload_file

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        result = upload_file(file.file)
        return {"url": result.get("secure_url") or result.get("url")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
