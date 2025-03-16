from fastapi import APIRouter, File, UploadFile
from engine.process_image import compress_image
from storage_connect import upload_to_supabase

photo_upload_router = APIRouter()

@photo_upload_router.post("/upload")
async def upload_photo(image: UploadFile = File(...)):
    image_byte = await image.read()
    image_compress = compress_image(image_bytes=image_byte)
    photo_url = upload_to_supabase(image_compress, image.filename)
    return {"photo_url": photo_url}
