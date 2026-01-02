"""
Utility functions for R2 bucket cleanup
"""
import os
import re
import logging
from urllib.parse import urlparse
from django.conf import settings
from django.core.files.storage import default_storage
from datetime import datetime, timedelta
from .upload_tracker import cleanup_unused_uploads, mark_upload_as_used, cleanup_old_tracking_records, delete_file_from_storage

logger = logging.getLogger(__name__)


def extract_images_from_html(html_content):
    """
    Extract image URLs from HTML content (CKEditor uploads).
    Returns a set of file paths relative to media root.
    Handles both relative URLs (/media/uploads/...) and absolute URLs (https://...).
    """
    if not html_content:
        return set()
    
    image_paths = set()
    
    # Find all img tags with src attributes
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    matches = re.findall(img_pattern, html_content, re.IGNORECASE)
    
    for url in matches:
        # Parse the URL
        parsed = urlparse(url)
        path = parsed.path
        
        # Handle different URL formats:
        # 1. Relative: /media/uploads/2024/01/15/image.jpg
        # 2. Absolute: https://media.domain.com/media/uploads/2024/01/15/image.jpg
        # 3. Absolute with custom domain: https://media.akusticnipanelieholux.com/media/uploads/...
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # Extract path after /media/ if present
        if '/media/' in path:
            path = path.split('/media/')[1]
        elif path.startswith('media/'):
            path = path[6:]  # Remove 'media/'
        
        # Only process uploads/ paths (CKEditor uploads)
        # Also handle direct uploads/ paths
        if path.startswith('uploads/'):
            image_paths.add(path)
    
    return image_paths




def cleanup_orphaned_images(model_instance, old_instance=None):
    """
    Clean up orphaned images when a model instance is saved or deleted.
    This includes:
    - Thumbnail images
    - Product gallery images
    - CKEditor uploaded images in descriptions
    
    Args:
        model_instance: The current instance being saved
        old_instance: The instance before save (for detecting changes)
    """
    # Only run cleanup in production (when using R2)
    if settings.DEBUG or not settings.AWS_ACCESS_KEY_ID:
        return
    
    # Get all current image paths from the instance
    current_image_paths = set()
    
    # Handle thumbnail (for both Product and BlogPost)
    if hasattr(model_instance, 'thumbnail') and model_instance.thumbnail:
        current_image_paths.add(model_instance.thumbnail.name)
    
    # Handle Product images (gallery)
    if hasattr(model_instance, 'images'):
        for img in model_instance.images.all():
            if img.image:
                current_image_paths.add(img.image.name)
    
    # Handle ProductPattern images
    if hasattr(model_instance, 'patterns'):
        for pattern in model_instance.patterns.all():
            if pattern.image:
                current_image_paths.add(pattern.image.name)
    
    # Handle CKEditor images in descriptions
    # Check short_description and full_description fields
    for field_name in ['short_description', 'full_description']:
        if hasattr(model_instance, field_name):
            field_value = getattr(model_instance, field_name)
            if field_value:
                ckeditor_images = extract_images_from_html(field_value)
                current_image_paths.update(ckeditor_images)
    
    # Get old image paths if old_instance exists
    old_image_paths = set()
    if old_instance:
        if hasattr(old_instance, 'thumbnail') and old_instance.thumbnail:
            old_image_paths.add(old_instance.thumbnail.name)
        
        if hasattr(old_instance, 'images'):
            for img in old_instance.images.all():
                if img.image:
                    old_image_paths.add(img.image.name)
        
        # Handle ProductPattern images from old instance
        if hasattr(old_instance, 'patterns'):
            for pattern in old_instance.patterns.all():
                if pattern.image:
                    old_image_paths.add(pattern.image.name)
        
        # Handle CKEditor images in old descriptions
        for field_name in ['short_description', 'full_description']:
            if hasattr(old_instance, field_name):
                field_value = getattr(old_instance, field_name)
                if field_value:
                    ckeditor_images = extract_images_from_html(field_value)
                    old_image_paths.update(ckeditor_images)
    
    # Find orphaned images (in old but not in current)
    orphaned_paths = old_image_paths - current_image_paths
    
    # Mark used uploads as used (for both new and edited instances)
    model_name = model_instance.__class__.__name__
    instance_id = model_instance.pk
    for path in current_image_paths:
        if path.startswith('uploads/'):
            try:
                mark_upload_as_used(path, model_name, instance_id)
            except Exception as e:
                # Log error but don't fail the save
                logger.warning(f"Failed to mark upload as used: {path} - {str(e)}")
    
    # Always cleanup unused uploads (for both new and edited instances)
    # This handles cases where images were uploaded but removed before saving
    # Pass old_instance info to help determine if this is a new instance
    is_new_instance = old_instance is None
    
    # For new instances, try to get session uploads if available
    # This allows us to check only uploads from current editing session
    session_uploads = None
    if is_new_instance:
        # Try to get request from model_instance (set by admin save_model)
        request = getattr(model_instance, '_request', None)
        if request and hasattr(request, 'session'):
            session_uploads = request.session.get('ckeditor_uploads', [])
    
    try:
        cleanup_unused_uploads(current_image_paths, model_name, instance_id, is_new_instance=is_new_instance, session_uploads=session_uploads)
    except Exception as e:
        # Log error but don't fail the save
        logger.warning(f"Failed to cleanup unused uploads: {str(e)}")
    
    # Clear session uploads after cleanup (for new instances)
    if is_new_instance and session_uploads is not None:
        request = getattr(model_instance, '_request', None)
        if request and hasattr(request, 'session'):
            request.session['ckeditor_uploads'] = []
            request.session.modified = True
    
    # Delete orphaned images (from old content that was removed)
    for path in orphaned_paths:
        delete_file_from_storage(path)
        
        # Also unmark tracking if this upload was tracked
        if path.startswith('uploads/'):
            from .models import CkeditorUpload
            try:
                upload = CkeditorUpload.objects.get(file_path=path)
                if upload.is_used and upload.used_in_id == instance_id:
                    # This upload was used in this instance but is now removed
                    upload.is_used = False
                    upload.used_in_model = ''
                    upload.used_in_id = None
                    upload.save()
            except CkeditorUpload.DoesNotExist:
                pass
    
    # Clean up old tracking records on every save
    # This is fast (just deleting old database records) and keeps the database clean
    try:
        cleanup_old_tracking_records()
    except Exception:
        pass  # Don't fail if cleanup has issues


def cleanup_all_instance_images(instance):
    """
    Clean up all images when an instance is deleted.
    This includes:
    - Thumbnail images
    - Product gallery images
    - CKEditor uploaded images in descriptions
    """
    # Only run cleanup in production (when using R2)
    if settings.DEBUG or not settings.AWS_ACCESS_KEY_ID:
        return
    
    image_paths = []
    
    # Handle thumbnail (for both Product and BlogPost)
    if hasattr(instance, 'thumbnail') and instance.thumbnail:
        image_paths.append(instance.thumbnail.name)
    
    # Handle Product images (gallery)
    if hasattr(instance, 'images'):
        for img in instance.images.all():
            if img.image:
                image_paths.append(img.image.name)
    
    # Handle ProductPattern images
    if hasattr(instance, 'patterns'):
        for pattern in instance.patterns.all():
            if pattern.image:
                image_paths.append(pattern.image.name)
    
    # Handle CKEditor images in descriptions
    for field_name in ['short_description', 'full_description']:
        if hasattr(instance, field_name):
            field_value = getattr(instance, field_name)
            if field_value:
                ckeditor_images = extract_images_from_html(field_value)
                image_paths.extend(ckeditor_images)
    
    # Delete all images
    for path in image_paths:
        delete_file_from_storage(path)


def cleanup_all_orphaned_files():
    """
    Scan entire R2 bucket and delete all files that are not referenced by any Product or BlogPost.
    This is a comprehensive cleanup that checks all files in the bucket.
    """
    # Import here to avoid circular imports
    from shop.models import Product, ProductImage
    from blog.models import BlogPost
    
    # Only run cleanup in production (when using R2)
    if settings.DEBUG or not settings.AWS_ACCESS_KEY_ID:
        return
    
    # Get all referenced image paths from database
    referenced_paths = set()
    
    # Get all product thumbnails
    for product in Product.objects.all():
        if product.thumbnail:
            referenced_paths.add(product.thumbnail.name)
    
    # Get all product gallery images
    for product_image in ProductImage.objects.all():
        if product_image.image:
            referenced_paths.add(product_image.image.name)
    
    # Get all blog thumbnails
    for blog in BlogPost.objects.all():
        if blog.thumbnail:
            referenced_paths.add(blog.thumbnail.name)
    
    # Get all CKEditor uploads (from full_description and short_description)
    # These are stored in the uploads/ path
    # Note: We can't easily track these without parsing HTML, so we'll skip them for now
    # or you can manually clean them up
    
    # List all files in the media/ directory in R2
    try:
        # Get all files from the media directory
        # This requires listing the bucket, which might be expensive
        # We'll focus on known paths: products/ and blog/
        
        # For now, we'll use a simpler approach:
        # Only check files in products/ and blog/ directories
        # and compare with database references
        
        # This is a simplified version - full bucket scan would require
        # listing all objects which can be slow and expensive
        
        # For comprehensive cleanup, you might want to run this as a management command
        # or scheduled task rather than on every save
        
        pass  # Full bucket listing would go here if needed
        
    except Exception as e:
        print(f"Error during full bucket cleanup: {e}")
    
    # The current per-instance cleanup is more efficient
    # Full bucket scans should be run manually or on a schedule

