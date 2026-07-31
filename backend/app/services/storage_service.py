import uuid

# pyrefly: ignore [missing-import]
from supabase import Client, create_client

from app.core.config import settings


class StorageService:
    def __init__(self):
        # Only initialize if URLs and keys are present
        if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
            # We use anon key or service role key. Service role key is better for backend operations.
            key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
            self.supabase: Client = create_client(settings.SUPABASE_URL, key)
        else:
            self.supabase = None
            
        self.default_bucket = "main-bucket"

    def upload_file(self, file_bytes: bytes, file_name: str, content_type: str, bucket: str | None = None) -> str:
        """
        Uploads a file to Supabase Storage and returns the public URL.
        """
        if not self.supabase:
            raise Exception("Supabase is not configured.")
            
        bucket_name = bucket or self.default_bucket
        
        # Ensure bucket exists (ideally done via migrations/setup, but good to note)
        
        # Generate a unique path to avoid collisions
        unique_id = str(uuid.uuid4())
        file_extension = file_name.split('.')[-1] if '.' in file_name else ''
        storage_path = f"{unique_id}.{file_extension}" if file_extension else unique_id

        # Upload the file
        self.supabase.storage.from_(bucket_name).upload(
            file=file_bytes,
            path=storage_path,
            file_options={"content-type": content_type}
        )
        
        # Get the public URL
        public_url = self.supabase.storage.from_(bucket_name).get_public_url(storage_path)
        return public_url

    def get_signed_url(self, file_path: str, bucket: str | None = None, expires_in: int = 3600) -> str:
        """
        Generates a signed URL for private files.
        """
        if not self.supabase:
            raise Exception("Supabase is not configured.")
            
        bucket_name = bucket or self.default_bucket
        res = self.supabase.storage.from_(bucket_name).create_signed_url(file_path, expires_in)
        return res['signedURL']

    def delete_file(self, file_path: str, bucket: str | None = None):
        """
        Deletes a file from Supabase Storage.
        """
        if not self.supabase:
            raise Exception("Supabase is not configured.")
            
        bucket_name = bucket or self.default_bucket
        self.supabase.storage.from_(bucket_name).remove([file_path])

storage_service = StorageService()
