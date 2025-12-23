from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from core.utils import cleanup_orphaned_images, cleanup_all_instance_images


class BlogPost(models.Model):
    title = models.CharField(_('Naslov'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    meta_title = models.CharField(_('Meta naslov'), max_length=200, blank=True)
    meta_description = models.TextField(_('Meta opis'), max_length=300, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to='blog/thumbnails/')
    short_description = models.TextField(_('Kratak opis'), max_length=500, default='')
    full_description = models.TextField(_('Pun opis'), default='')
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Blog post')
        verbose_name_plural = _('Blog postovi')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Store old instance for cleanup
        old_instance = None
        if self.pk:
            try:
                old_instance = BlogPost.objects.get(pk=self.pk)
            except BlogPost.DoesNotExist:
                pass
        
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        
        super().save(*args, **kwargs)
        
        # Cleanup orphaned images after save
        # For new instances (old_instance is None), cleanup will check for orphaned uploads
        cleanup_orphaned_images(self, old_instance)


@receiver(post_delete, sender=BlogPost)
def blog_post_delete_handler(sender, instance, **kwargs):
    """Clean up images when blog post is deleted"""
    cleanup_all_instance_images(instance)
