import os
from django.core.files.storage import Storage
from supabase import create_client


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")

client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    def _save(self, name, content):
        # Normalize name for Supabase
        name = name.replace("\\", "/")
        file_bytes = content.read()

        response = client.storage.from_(SUPABASE_BUCKET).upload(
            file=name,
            file=file_bytes,
            file_options={"content-type": content.content_type},
        )

        if response is None or getattr(response, "error", None):
            raise Exception(f"Supabase upload failed: {response.error}")

        return name

    def url(self, name):
        name = name.replace("\\", "/")
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"

    def exists(self, name):
        # Django checks this before saving. Always return False.
        return False