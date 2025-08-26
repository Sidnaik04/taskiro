import cloudinary
import cloudinary.uploader
import os
from ..config import settings


def configure_cloudinary():
    # The SDK will also pick up CLOUDINARY_URL env var automatically.
    url = settings.cloudinary_url or os.getenv("CLOUDINARY_URL")
    if url:
        cloudinary.config(cloudinary_url=url)


def upload_file(file_obj, folder: str = "tasks"):
    configure_cloudinary()
    return cloudinary.uploader.upload(file_obj, folder=folder)
