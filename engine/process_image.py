import io
from PIL import Image

def compress_image(image_bytes, quality=50):
    _image = Image.open(io.BytesIO(image_bytes))
    _image = _image.convert("RGB")
    _compress_image_io = io.BytesIO()  # Create a BytesIO buffer
    _image.save(_compress_image_io, "JPEG", quality=quality)
    _compress_image_io.seek(0)  # Reset buffer position to the beginning
    return _compress_image_io

