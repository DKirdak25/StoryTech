import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseStorage(Storage):

    def _save(self, name, content):
        data = content.read()
        client.storage.from_(SUPABASE_BUCKET).upload(name, data)
        return name

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"

    def exists(self, name):
        return False