import os
from utils import generate_uuid
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def upload_to_supabase(compressed_io, image_filename, bucket_name="app_file"):
    """Upload compressed image to Supabase Storage and return the public URL."""
    try:
        # Generate a unique filename
        image_filename = f"{generate_uuid()}|{image_filename}"  

        # Upload to Supabase Storage
        response = supabase.storage.from_(bucket_name).upload(
            path=image_filename,
            file=compressed_io.getvalue(),
            file_options={"content-type": "image/jpeg"}
        )

        # Check for errors
        if response.get("error"):
            print(f"Upload error: {response['error']}")
            return None

        # Get public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(image_filename)
        return public_url

    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        return None
