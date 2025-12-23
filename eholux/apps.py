from django.apps import AppConfig


class EholuxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eholux'
    
    def ready(self):
        import eholux.admin
        # Patch CKEditor to support WebP format
        try:
            import ckeditor_uploader.utils
            ckeditor_uploader.utils.IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        except ImportError:
            pass

