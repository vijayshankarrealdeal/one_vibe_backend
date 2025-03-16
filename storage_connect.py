import os
from utils import generate_uuid, sanitize_filename
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()


supabase = create_client(
    supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxZXNjeGlydnB2YmpraWZicnd1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNzk4ODIzMSwiZXhwIjoyMDUzNTY0MjMxfQ.pPcKMqJD30Iv2dhmpUr48fUGrtcR3LS9TgkFEn2_FlA",
    supabase_url="https://iqescxirvpvbjkifbrwu.supabase.co"
)




def upload_to_supabase(compressed_io, image_filename, bucket_name="ov"):
    """Upload compressed image to Supabase Storage and return the public URL."""
    try:
        # Generate a unique filename
        unique_key = ''.join(generate_uuid().split('-'))
        image_filename = sanitize_filename(f"{unique_key}|{image_filename}")

        # Upload to Supabase Storage

        path=f'app_files/{image_filename}'
        response = supabase.storage.from_(bucket_name).upload(
            path=path,
            file=compressed_io.getvalue(),
            file_options={"content-type": "image/jpeg"}
        )        
        public_url = supabase.storage.from_(bucket_name).get_public_url(response.path)
        return public_url
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        return None
