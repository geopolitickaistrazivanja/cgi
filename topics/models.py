from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from core.utils import (
    cleanup_orphaned_images, 
    cleanup_all_instance_images,
    unique_topic_thumbnail,
    unique_category_thumbnail
)


class Category(models.Model):
    name = models.CharField(_('Naziv'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=unique_category_thumbnail)
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Store old instance for cleanup
        old_instance = None
        if self.pk:
            try:
                old_instance = Category.objects.get(pk=self.pk)
            except Category.DoesNotExist:
                pass
        
        if not self.slug:
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)
        
        # Cleanup orphaned images after save (when thumbnail is replaced)
        cleanup_orphaned_images(self, old_instance)


@receiver(post_delete, sender=Category)
def category_delete_handler(sender, instance, **kwargs):
    """Clean up images when category is deleted"""
    cleanup_all_instance_images(instance)


class Topic(models.Model):
    title = models.CharField(_('Naslov'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='topics', verbose_name=_('Kategorija'))
    meta_title = models.CharField(_('Meta naslov'), max_length=200, blank=True)
    meta_description = models.TextField(_('Meta opis'), max_length=300, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=unique_topic_thumbnail)
    short_description = models.TextField(_('Kratak opis'), max_length=500, default='')
    full_description = models.TextField(_('Pun opis'), default='')
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Store old instance for cleanup
        old_instance = None
        if self.pk:
            try:
                old_instance = Topic.objects.get(pk=self.pk)
            except Topic.DoesNotExist:
                pass
        
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        
        super().save(*args, **kwargs)
        
        # Cleanup orphaned images after save
        # For new instances (old_instance is None), cleanup will check for orphaned uploads
        cleanup_orphaned_images(self, old_instance)


@receiver(post_delete, sender=Topic)
def topic_delete_handler(sender, instance, **kwargs):
    """Clean up images when topic is deleted"""
    cleanup_all_instance_images(instance)
