import dropbox
import dropbox
import os
from utils import generate_uuid
from dotenv import load_dotenv
load_dotenv()

dropbox_access_token = os.environ.get("DROPBOX_ACCESS_TOKEN", None)
dbx = dropbox.Dropbox(dropbox_access_token)
def upload_to_dropbox(compress_image_io, image_filename):
    image_filename = f"{generate_uuid()}|{image_filename}" 
    dropbox_path = f"/app_file/{image_filename}"
    dbx.files_upload(compress_image_io.getvalue(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))

    # Create a shared link
    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
    print(shared_link_metadata)
    direct_download_url = shared_link_metadata.url.replace("=0", "=1")
    return direct_download_url