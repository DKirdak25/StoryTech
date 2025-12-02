import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    def _save(self, name, content):
        # Read bytes
        file_bytes = content.read()

        # Correct Supabase upload call (v2)
        response = client.storage \
            .from_(SUPABASE_BUCKET) \
            .upload(
                path=name,
                file=file_bytes,
                file_options={"content-type": content.content_type}
            )

        # Check for errors
        if "error" in response and response["error"]:
            raise Exception(f"Supabase Upload Failed: {response['error']['message']}")

        return name

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"

    def exists(self, name):
        # Always overwrite
        return False