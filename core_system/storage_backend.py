import os
from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Correct setting names
SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
SUPABASE_BUCKET = settings.SUPABASE_BUCKET

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):
    """
    Django Storage backend for Supabase Storage.
    """

    def _save(self, name, content):
        data = content.read()

        try:
            client.storage.from_(SUPABASE_BUCKET).upload(
                name,
                data,
                {"content-type": getattr(content, "content_type", "application/octet-stream")}
            )
            return name
        except Exception:
            logger.exception("Upload to Supabase failed for %s", name)
            raise

    def open(self, name, mode="rb"):
        try:
            data = client.storage.from_(SUPABASE_BUCKET).download(name)
            return data
        except Exception:
            logger.exception("Download from Supabase failed for %s", name)
            raise

    def url(self, name):
        try:
            # get_public_url returns a string → so return directly
            return client.storage.from_(SUPABASE_BUCKET).get_public_url(name)
        except Exception:
            logger.exception("Failed generating Supabase public URL for %s", name)
            return ""

    def exists(self, name):
        try:
            files = client.storage.from_(SUPABASE_BUCKET).list()
            return any(f.get("name") == name for f in files)
        except Exception:
            logger.exception("Failed checking existence of %s", name)
            return False