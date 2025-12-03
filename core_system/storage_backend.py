import logging
logger = logging.getLogger(__name__)

class SupabaseStorage(Storage):

    def _save(self, name, content):
        try:
            name = name.replace("\\", "/")
            file_bytes = content.read()
            mime_type = getattr(content, "content_type", "application/octet-stream")

            response = client.storage.from_(SUPABASE_BUCKET).upload(
                file=name,
                file=file_bytes,
                file_options={
                    "content-type": mime_type,
                    "upsert": False,
                },
            )

            if getattr(response, "error", None):
                logger.error(f"SUPABASE UPLOAD ERROR: {response.error}")
                raise Exception(f"Supabase upload failed: {response.error}")

            return name

        except Exception as e:
            logger.exception(f"STORAGE ERROR during upload of {name}")
            raise