from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
SUPABASE_BUCKET = settings.SUPABASE_BUCKET

class SupabaseStorage(Storage):

    def _save(self, name, content):
        try:
            name = name.replace("\\", "/")
            file_bytes = content.read()
            mime_type = getattr(content, "content_type", "application/octet-stream")

            response = client.storage.from_(SUPABASE_BUCKET).upload(
                path=name,
                file=file_bytes,
                file_options={
                    "content-type": mime_type,
                },
            )

            if hasattr(response, "error") and response.error:
                logger.error(f"SUPABASE UPLOAD ERROR: {response.error}")
                raise Exception(f"Supabase upload failed: {response.error}")

            return name

        except Exception:
            logger.exception(f"STORAGE ERROR during upload of %s", name)
            raise
     
    def exists(self, name):
        """
        Always return False so Django never tries to append unique suffixes.
        Supabase handles paths without overwriting unless upsert=True.
        """
        return False

    def url(self, name):
    try:
        # Supabase returns a string, not a dict
        public_url = client.storage.from_(SUPABASE_BUCKET).get_public_url(name)
        return public_url
    except Exception:
        logger.exception("Failed generating Supabase public URL for %s", name)
        return ""