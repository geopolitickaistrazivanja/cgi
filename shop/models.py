from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.utils import cleanup_orphaned_images, cleanup_all_instance_images


class Category(models.Model):
    name = models.CharField(_('Naziv'), max_length=200, unique=True)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Kategorija')
        verbose_name_plural = _('Kategorije')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    name = models.CharField(_('Naziv atributa'), max_length=200, unique=True)
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)

    class Meta:
        verbose_name = _('Atribut proizvoda')
        verbose_name_plural = _('Atributi proizvoda')
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('Slika'), upload_to='products/')
    alt_text = models.CharField(_('Alternativni tekst'), max_length=200, blank=True)
    order = models.PositiveIntegerField(_('Redosled'), default=0)

    class Meta:
        verbose_name = _('Slika proizvoda')
        verbose_name_plural = _('Slike proizvoda')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.product.title} - Slika {self.order + 1}"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey('Product', related_name='attribute_values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.TextField(_('Vrednost'))

    class Meta:
        verbose_name = _('Vrednost atributa')
        verbose_name_plural = _('Vrednosti atributa')
        unique_together = ['product', 'attribute']

    def __str__(self):
        return f"{self.product.title} - {self.attribute.name}: {self.value}"


class Product(models.Model):
    STOCK_CHOICES = [
        ('always', _('Uvek na stanju')),
        ('limited', _('Ograničena količina')),
    ]

    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    meta_title = models.CharField(_('Meta naslov'), max_length=200)
    meta_description = models.TextField(_('Meta opis'), max_length=300)
    sku = models.CharField(_('SKU'), max_length=100, unique=True)
    title = models.CharField(_('Naziv'), max_length=200)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to='products/thumbnails/', blank=True, null=True)
    short_description = models.TextField(_('Kratak opis'), max_length=500)
    full_description = models.TextField(_('Pun opis'))
    price = models.DecimalField(_('Cena'), max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(_('Cena na popustu'), max_digits=10, decimal_places=2, null=True, blank=True)
    
    stock_type = models.CharField(_('Tip zaliha'), max_length=10, choices=STOCK_CHOICES, default='always')
    stock_quantity = models.PositiveIntegerField(_('Količina na stanju'), null=True, blank=True)
    is_active = models.BooleanField(_('Aktivan'), default=True)
    
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Proizvod')
        verbose_name_plural = _('Proizvodi')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Store old instance for cleanup
        old_instance = None
        if self.pk:
            try:
                old_instance = Product.objects.get(pk=self.pk)
            except Product.DoesNotExist:
                pass
        
        if not self.slug:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
        
        # Cleanup orphaned images after save
        # For new instances (old_instance is None), cleanup will check for orphaned uploads
        cleanup_orphaned_images(self, old_instance)

    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def is_in_stock(self):
        if self.stock_type == 'always':
            return True
        return self.stock_quantity and self.stock_quantity > 0

    @property
    def main_image(self):
        """Returns thumbnail if available, otherwise first gallery image"""
        if self.thumbnail:
            return self.thumbnail
        return self.images.first()

    def decrease_stock(self, quantity=1):
        """Decrease stock and send email if out of stock"""
        if self.stock_type == 'limited' and self.stock_quantity:
            self.stock_quantity -= quantity
            if self.stock_quantity <= 0:
                self.stock_quantity = 0
                self.is_active = False
                # Send email notification
                try:
                    send_mail(
                        subject='Proizvod nije više na stanju',
                        message=f'Proizvod "{self.title}" (SKU: {self.sku}) više nije na stanju.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_EMAIL],
                        fail_silently=True,
                    )
                except Exception:
                    pass
            self.save()


@receiver(post_delete, sender=Product)
def product_delete_handler(sender, instance, **kwargs):
    """Clean up images when product is deleted"""
    cleanup_all_instance_images(instance)


@receiver(post_delete, sender=ProductImage)
def product_image_delete_handler(sender, instance, **kwargs):
    """Clean up image file when ProductImage is deleted"""
    from core.utils import delete_file_from_storage
    if instance.image:
        delete_file_from_storage(instance.image.name)
