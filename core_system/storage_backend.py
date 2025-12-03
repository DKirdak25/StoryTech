import os
from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_SECRET_KEY
SUPABASE_BUCKET = settings.SUPABASE_BUCKET_NAME

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    """
    Django Storage backend for Supabase Storage.
    Provides:
    - save
    - open
    - url
    - exists
    """

    def _save(self, name, content):
        data = content.read()

        try:
            response = client.storage.from_(SUPABASE_BUCKET).upload(
                path=name,
                file=data,
                file_options={"content-type": content.content_type}
            )
            return name
        except Exception:
            logger.exception("Upload to Supabase failed for %s", name)
            raise

    def open(self, name, mode="rb"):
        try:
            res = client.storage.from_(SUPABASE_BUCKET).download(name)
            return res
        except Exception:
            logger.exception("Download from Supabase failed for %s", name)
            raise

    def url(self, name):
        """
        Supabase Python SDK returns a **string**, not a dict.
        """
        try:
            public_url = client.storage.from_(SUPABASE_BUCKET).get_public_url(name)
            return public_url
        except Exception:
            logger.exception("Failed generating Supabase public URL for %s", name)
            return ""

    def exists(self, name):
        # Supabase does not provide direct exists(), so list them
        try:
            files = client.storage.from_(SUPABASE_BUCKET).list()
            return any(f.get("name") == name for f in files)
        except Exception:
            logger.exception("Failed checking existence of %s", name)
            return False