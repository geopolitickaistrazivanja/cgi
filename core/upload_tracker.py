"""
Track CKEditor uploads to enable orphaned file cleanup.
"""
from django.conf import settings
from django.core.files.storage import default_storage
from .models import CkeditorUpload
import os


def delete_file_from_storage(file_path):
    """
    Delete a file from storage (R2 in production, local in development).
    Moved here to avoid circular imports.
    """
    if not file_path:
        return False
    
    try:
        # Check if file exists and delete it
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            return True
    except Exception as e:
        # Log error but don't fail
        print(f"Error deleting file {file_path}: {e}")
        return False
    
    return False


def track_upload(file_path, user=None):
    """
    Track a CKEditor upload.
    
    Args:
        file_path: Path to the uploaded file (relative to media root)
        user: User who uploaded the file (optional)
    """
    # Normalize path (remove leading slash, ensure consistent format)
    if file_path.startswith('/'):
        file_path = file_path[1:]
    
    # Only track uploads/ paths (CKEditor uploads)
    if not file_path.startswith('uploads/'):
        return
    
    # Create or update tracking record
    upload, created = CkeditorUpload.objects.get_or_create(
        file_path=file_path,
        defaults={
            'uploaded_by': user,
            'is_used': False,
        }
    )
    
    # If already exists but not used, reset it (new upload session)
    if not created and not upload.is_used:
        upload.uploaded_by = user
        upload.uploaded_at = upload.uploaded_at  # Keep original upload time
        upload.save()


def mark_upload_as_used(file_path, model_name, instance_id):
    """
    Mark an upload as used in a specific model instance.
    
    Args:
        file_path: Path to the file
        model_name: Name of the model ('Product' or 'BlogPost')
        instance_id: ID of the instance
    """
    # Normalize path
    if file_path.startswith('/'):
        file_path = file_path[1:]
    
    if not file_path.startswith('uploads/'):
        return
    
    try:
        # Try to get the upload (whether used or not)
        upload = CkeditorUpload.objects.get(file_path=file_path)
        # Update it to mark as used (even if already used, update the reference)
        upload.is_used = True
        upload.used_in_model = model_name
        upload.used_in_id = instance_id
        upload.save()
    except CkeditorUpload.DoesNotExist:
        # File was uploaded but not tracked (e.g., before tracking was implemented)
        # Create tracking record as used
        CkeditorUpload.objects.create(
            file_path=file_path,
            is_used=True,
            used_in_model=model_name,
            used_in_id=instance_id,
        )
    except CkeditorUpload.MultipleObjectsReturned:
        # Handle case where multiple records exist (shouldn't happen, but be safe)
        # Get the first one and update it, delete the rest
        uploads = CkeditorUpload.objects.filter(file_path=file_path)
        upload = uploads.first()
        upload.is_used = True
        upload.used_in_model = model_name
        upload.used_in_id = instance_id
        upload.save()
        # Delete duplicates
        uploads.exclude(pk=upload.pk).delete()


def cleanup_unused_uploads(referenced_paths, model_name=None, instance_id=None):
    """
    Clean up uploads that were tracked but not used in ANY product/blog.
    Deletes orphaned files with a grace period to avoid deleting files that are still being edited.
    
    This handles cases where:
    - Images were uploaded but removed from CKEditor before saving
    - Images were uploaded, saved, then removed from CKEditor and saved again
    - Images were uploaded but never used in any content
    
    Args:
        referenced_paths: Set of file paths from the current instance being saved
        model_name: Name of the model being saved (optional)
        instance_id: ID of the instance being saved (optional)
    """
    from datetime import timedelta
    from django.utils import timezone
    
    # Grace period: Don't delete uploads that are less than 5 minutes old
    # This prevents deleting files that user just uploaded and might still be editing
    grace_period = timezone.now() - timedelta(minutes=5)
    
    # Get ALL referenced paths from ALL products and blogs in database
    # This ensures we don't delete files that are used in other products/blogs
    from shop.models import Product
    from blog.models import BlogPost
    from core.utils import extract_images_from_html
    
    all_referenced_paths = set()
    
    # Get all images from all products
    for product in Product.objects.all():
        for field_name in ['short_description', 'full_description']:
            field_value = getattr(product, field_name, '')
            if field_value:
                images = extract_images_from_html(field_value)
                all_referenced_paths.update(images)
    
    # Get all images from all blogs
    for blog in BlogPost.objects.all():
        for field_name in ['short_description', 'full_description']:
            field_value = getattr(blog, field_name, '')
            if field_value:
                images = extract_images_from_html(field_value)
                all_referenced_paths.update(images)
    
    # Also add paths from the current instance being saved
    normalized_referenced = set()
    for path in referenced_paths:
        if path.startswith('/'):
            path = path[1:]
        if path.startswith('uploads/'):
            normalized_referenced.add(path)
    
    all_referenced_paths.update(normalized_referenced)
    
    deleted_count = 0
    
    # Clean up unused uploads (never saved in any content)
    # Only delete if they're older than grace period (5 minutes)
    # This handles: images uploaded but removed from CKEditor before saving
    unused_uploads = CkeditorUpload.objects.filter(
        is_used=False,
        uploaded_at__lt=grace_period  # Only check uploads older than 5 minutes
    )
    
    for upload in unused_uploads:
        # Check if this upload is used in ANY product/blog
        if upload.file_path not in all_referenced_paths:
            # This upload is truly orphaned - delete it
            if delete_file_from_storage(upload.file_path):
                deleted_count += 1
            # Delete the tracking record
            upload.delete()
    
    # Also check used uploads that are no longer referenced
    # This handles cases where images were saved, then removed from content
    # Only check uploads that were used in the current instance (more efficient)
    if model_name and instance_id:
        # Check uploads that were used in this specific instance
        instance_used_uploads = CkeditorUpload.objects.filter(
            is_used=True,
            used_in_model=model_name,
            used_in_id=instance_id
        )
        for upload in instance_used_uploads:
            if upload.file_path not in all_referenced_paths:
                # This upload was used in this instance but is no longer referenced - delete it
                if delete_file_from_storage(upload.file_path):
                    deleted_count += 1
                # Delete the tracking record
                upload.delete()
    
    return deleted_count


def cleanup_old_tracking_records():
    """
    Clean up old tracking records to keep the database clean.
    This runs automatically on every product/blog save.
    
    Deletes:
    - Used records older than 7 days (file stays in R2, just removes tracking record)
    - Unused records are deleted immediately when orphaned (handled in cleanup_unused_uploads)
    """
    from datetime import timedelta
    from django.utils import timezone
    
    cutoff = timezone.now() - timedelta(days=7)
    
    # Delete old used records (older than 7 days)
    # These are safe to delete - the file is already used and saved in a product/blog
    # We only delete the tracking record, the file stays in R2
    deleted_used = CkeditorUpload.objects.filter(
        is_used=True,
        uploaded_at__lt=cutoff
    ).delete()[0]
    
    # Unused records are now deleted immediately when they become orphaned
    # (handled in cleanup_unused_uploads function)
    # No need to wait 30 days - they're deleted right away
    
    return deleted_used, 0

