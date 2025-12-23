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


@method_decorator(csrf_exempt, name='dispatch')
class TrackedImageUploadView(ImageUploadView):
    """
    Custom upload view that tracks uploads for cleanup.
    Extends the default CKEditor ImageUploadView.
    """
    
    def post(self, request, **kwargs):
        """
        Uploads a file and tracks it for orphaned file cleanup.
        """
        uploaded_file = request.FILES["upload"]
        
        backend = get_backend()
        storage = utils.storage
        
        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)
        
        filewrapper = backend(storage, uploaded_file)
        allow_nonimages = getattr(settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
        
        # Throws an error when an non-image file are uploaded.
        if not filewrapper.is_image and not allow_nonimages:
            return HttpResponse(
                """
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '', 'Invalid file type.');
                </script>""".format(
                    ck_func_num
                )
            )
        
        filepath = get_upload_filename(uploaded_file.name, request)
        saved_path = filewrapper.save_as(filepath)
        
        # Track the upload
        # saved_path is relative to media root (e.g., "uploads/2024/01/15/image.jpg")
        track_upload(saved_path, user=request.user if request.user.is_authenticated else None)
        
        url = utils.get_media_url(saved_path)
        
        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '{}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            _, filename = os.path.split(saved_path)
            retdata = {"url": url, "uploaded": "1", "fileName": filename}
            return JsonResponse(retdata)

