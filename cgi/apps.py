from django.apps import AppConfig


class CgiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cgi'
    
    def ready(self):
        import cgi.admin
        # Patch CKEditor to support WebP format
        try:
            import ckeditor_uploader.utils
            ckeditor_uploader.utils.IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        except ImportError:
            pass

