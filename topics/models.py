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
    # Serbian Latin (default)
    name = models.CharField(_('Naziv'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    
    # Serbian Cyrillic
    name_sr_cyrl = models.CharField(_('Naziv (ћирилица)'), max_length=200, blank=True)
    slug_sr_cyrl = models.SlugField(_('Slug (ћирилица)'), max_length=200, blank=True)
    
    # English
    name_en = models.CharField(_('Name (English)'), max_length=200, blank=True)
    slug_en = models.SlugField(_('Slug (English)'), max_length=200, blank=True)
    
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=unique_category_thumbnail)
    order = models.IntegerField(_('Redosled'), default=0, help_text=_('Koristi se za sortiranje kategorija u padajućem meniju'))
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    def get_name(self):
        """Get name based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.name_sr_cyrl:
            return self.name_sr_cyrl
        elif lang == 'en' and self.name_en:
            return self.name_en
        return self.name
    
    def get_slug(self):
        """Get slug based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.slug_sr_cyrl:
            return self.slug_sr_cyrl
        elif lang == 'en' and self.slug_en:
            return self.slug_en
        return self.slug

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
        if not self.slug_sr_cyrl and self.name_sr_cyrl:
            self.slug_sr_cyrl = slugify(self.name_sr_cyrl)
        if not self.slug_en and self.name_en:
            self.slug_en = slugify(self.name_en)
        
        super().save(*args, **kwargs)
        
        # Cleanup orphaned images after save (when thumbnail is replaced)
        cleanup_orphaned_images(self, old_instance)


@receiver(post_delete, sender=Category)
def category_delete_handler(sender, instance, **kwargs):
    """Clean up images when category is deleted"""
    cleanup_all_instance_images(instance)


class Topic(models.Model):
    # Serbian Latin (default)
    title = models.CharField(_('Naslov'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    meta_title = models.CharField(_('Meta naslov'), max_length=200, blank=True)
    meta_description = models.TextField(_('Meta opis'), max_length=300, blank=True)
    short_description = models.TextField(_('Kratak opis'), max_length=500, default='')
    full_description = models.TextField(_('Pun opis'), default='')
    
    # Serbian Cyrillic
    title_sr_cyrl = models.CharField(_('Naslov (ћирилица)'), max_length=200, blank=True)
    slug_sr_cyrl = models.SlugField(_('Slug (ћирилица)'), max_length=200, blank=True)
    meta_title_sr_cyrl = models.CharField(_('Meta naslov (ћирилица)'), max_length=200, blank=True)
    meta_description_sr_cyrl = models.TextField(_('Meta opis (ћирилица)'), max_length=300, blank=True)
    short_description_sr_cyrl = models.TextField(_('Kratak opis (ћирилица)'), max_length=500, default='', blank=True)
    full_description_sr_cyrl = models.TextField(_('Pun opis (ћирилица)'), default='', blank=True)
    
    # English
    title_en = models.CharField(_('Title (English)'), max_length=200, blank=True)
    slug_en = models.SlugField(_('Slug (English)'), max_length=200, blank=True)
    meta_title_en = models.CharField(_('Meta title (English)'), max_length=200, blank=True)
    meta_description_en = models.TextField(_('Meta description (English)'), max_length=300, blank=True)
    short_description_en = models.TextField(_('Short description (English)'), max_length=500, default='', blank=True)
    full_description_en = models.TextField(_('Full description (English)'), default='', blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='topics', verbose_name=_('Kategorija'))
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=unique_topic_thumbnail)
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_title(self):
        """Get title based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.title_sr_cyrl:
            return self.title_sr_cyrl
        elif lang == 'en' and self.title_en:
            return self.title_en
        return self.title
    
    def get_slug(self):
        """Get slug based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.slug_sr_cyrl:
            return self.slug_sr_cyrl
        elif lang == 'en' and self.slug_en:
            return self.slug_en
        return self.slug
    
    def get_meta_title(self):
        """Get meta_title based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.meta_title_sr_cyrl:
            return self.meta_title_sr_cyrl
        elif lang == 'en' and self.meta_title_en:
            return self.meta_title_en
        return self.meta_title or self.get_title()
    
    def get_meta_description(self):
        """Get meta_description based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.meta_description_sr_cyrl:
            return self.meta_description_sr_cyrl
        elif lang == 'en' and self.meta_description_en:
            return self.meta_description_en
        return self.meta_description
    
    def get_short_description(self):
        """Get short_description based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.short_description_sr_cyrl:
            return self.short_description_sr_cyrl
        elif lang == 'en' and self.short_description_en:
            return self.short_description_en
        return self.short_description
    
    def get_full_description(self):
        """Get full_description based on current language"""
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'sr-cyrl' and self.full_description_sr_cyrl:
            return self.full_description_sr_cyrl
        elif lang == 'en' and self.full_description_en:
            return self.full_description_en
        return self.full_description

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
        if not self.slug_sr_cyrl and self.title_sr_cyrl:
            self.slug_sr_cyrl = slugify(self.title_sr_cyrl)
        if not self.slug_en and self.title_en:
            self.slug_en = slugify(self.title_en)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_title_sr_cyrl and self.title_sr_cyrl:
            self.meta_title_sr_cyrl = self.title_sr_cyrl
        if not self.meta_title_en and self.title_en:
            self.meta_title_en = self.title_en
        
        super().save(*args, **kwargs)
        
        # Cleanup orphaned images after save
        # For new instances (old_instance is None), cleanup will check for orphaned uploads
        cleanup_orphaned_images(self, old_instance)


@receiver(post_delete, sender=Topic)
def topic_delete_handler(sender, instance, **kwargs):
    """Clean up images when topic is deleted"""
    cleanup_all_instance_images(instance)
