"""
Custom CKEditor upload view that tracks uploads for orphaned file cleanup.
"""
from ckeditor_uploader.views import ImageUploadView, get_upload_filename
from ckeditor_uploader.backends import get_backend
from ckeditor_uploader import utils
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .upload_tracker import track_upload
import os
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TrackedImageUploadView(ImageUploadView):
    """
    Custom upload view that tracks uploads for cleanup.
    Extends the default CKEditor ImageUploadView.
    """
    
    def post(self, request, **kwargs):
        """
        Uploads a file and tracks it for orphaned file cleanup.
        Returns JSON response for modern CKEditor (6.7.0+).
        """
        try:
            # Check if user is authenticated (required for admin)
            if not request.user.is_authenticated:
                error_msg = "Authentication required."
                return JsonResponse({
                    "uploaded": 0,
                    "error": {
                        "message": error_msg
                    }
                }, status=403)
            
            # Check if upload file exists
            if "upload" not in request.FILES:
                return JsonResponse({
                    "uploaded": 0,
                    "error": {
                        "message": "No file uploaded."
                    }
                }, status=400)
            
            uploaded_file = request.FILES["upload"]
            
            backend = get_backend()
            storage = utils.storage
            
            ck_func_num = request.GET.get("CKEditorFuncNum")
            if ck_func_num:
                ck_func_num = escape(ck_func_num)
            
            # Ensure WebP is in the allowed image extensions (patch might not be applied yet)
            if not hasattr(utils, 'IMAGE_EXTENSIONS') or '.webp' not in utils.IMAGE_EXTENSIONS:
                utils.IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
            
            filewrapper = backend(storage, uploaded_file)
            allow_nonimages = getattr(settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
            
            # Check file extension for image types (including WebP)
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
            is_image_by_extension = file_extension in image_extensions
            
            # Check if file is an image (use both filewrapper check and extension check)
            # This ensures WebP files are recognized even if filewrapper doesn't recognize them
            if not (filewrapper.is_image or is_image_by_extension) and not allow_nonimages:
                error_msg = "Invalid file type. Only image files are allowed."
                if ck_func_num:
                    # Legacy format for old CKEditor
                    return HttpResponse(
                        """
                        <script type='text/javascript'>
                        window.parent.CKEDITOR.tools.callFunction({}, '', '{}');
                        </script>""".format(
                            ck_func_num, error_msg
                        )
                    )
                else:
                    # Modern JSON format
                    return JsonResponse({
                        "uploaded": 0,
                        "error": {
                            "message": error_msg
                        }
                    }, status=400)
            
            # Generate filepath and save
            filepath = get_upload_filename(uploaded_file.name, request)
            saved_path = filewrapper.save_as(filepath)
            
            # Track the upload in database (for general tracking)
            # saved_path is relative to media root (e.g., "uploads/2024/01/15/image.jpg")
            try:
                track_upload(saved_path, user=request.user if request.user.is_authenticated else None)
            except Exception as e:
                # Log tracking error but don't fail the upload
                logger.warning(f"Failed to track upload {saved_path}: {str(e)}")
            
            # Also track in session for this editing session
            # This allows us to check only uploads from current editing session when saving
            if 'ckeditor_uploads' not in request.session:
                request.session['ckeditor_uploads'] = []
            
            # Add this upload to session (store the file path)
            if saved_path not in request.session['ckeditor_uploads']:
                request.session['ckeditor_uploads'].append(saved_path)
                request.session.modified = True  # Mark session as modified
            
            # Get the URL for the uploaded file
            url = utils.get_media_url(saved_path)
            
            # Ensure URL is absolute (CKEditor needs absolute URLs)
            if not url.startswith('http'):
                # Use request to build absolute URL
                url = request.build_absolute_uri(url)
            
            _, filename = os.path.split(saved_path)
            
            if ck_func_num:
                # Legacy format for old CKEditor (JavaScript callback)
                return HttpResponse(
                    """
                    <script type='text/javascript'>
                        window.parent.CKEDITOR.tools.callFunction({}, '{}');
                    </script>""".format(
                        ck_func_num, url
                    )
                )
            else:
                # Modern JSON format for CKEditor 6.7.0+
                return JsonResponse({
                    "uploaded": 1,
                    "fileName": filename,
                    "url": url
                })
                
        except Exception as e:
            # Log the error for debugging
            logger.error(f"CKEditor upload error: {str(e)}", exc_info=True)
            
            error_msg = f"Upload failed: {str(e)}"
            
            # Check if it's the old format
            ck_func_num = request.GET.get("CKEditorFuncNum")
            if ck_func_num:
                ck_func_num = escape(ck_func_num)
                return HttpResponse(
                    """
                    <script type='text/javascript'>
                    window.parent.CKEDITOR.tools.callFunction({}, '', '{}');
                    </script>""".format(
                        ck_func_num, error_msg
                    )
                )
            else:
                # Modern JSON format with error
                return JsonResponse({
                    "uploaded": 0,
                    "error": {
                        "message": error_msg
                    }
                }, status=500)

