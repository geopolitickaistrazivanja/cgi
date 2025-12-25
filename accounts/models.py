from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(_('Telefon'), max_length=20, blank=True)
    address = models.TextField(_('Adresa'), blank=True)
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Profil korisnika')
        verbose_name_plural = _('Profili korisnika')

    def __str__(self):
        return f"{self.user.username} - Profil"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Na čekanju')),
        ('processing', _('U obradi')),
        ('completed', _('Završeno')),
        ('cancelled', _('Otkazano')),
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(_('Email'))
    first_name = models.CharField(_('Ime'), max_length=100)
    last_name = models.CharField(_('Prezime'), max_length=100)
    phone = models.CharField(_('Telefon'), max_length=20)
    address = models.TextField(_('Adresa'))
    city = models.CharField(_('Grad'), max_length=100)
    postal_code = models.CharField(_('Poštanski broj'), max_length=20)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(_('Ukupan iznos'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('Kreirano'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ažurirano'), auto_now=True)

    class Meta:
        verbose_name = _('Porudžbina')
        verbose_name_plural = _('Porudžbine')
        ordering = ['-created_at']

    def __str__(self):
        return f"Porudžbina #{self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Količina'))
    price = models.DecimalField(_('Cena'), max_digits=10, decimal_places=2)
    # Selected dimension and pattern
    selected_dimension = models.ForeignKey('shop.ProductDimension', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Izabrane dimenzije'))
    selected_pattern = models.ForeignKey('shop.ProductPattern', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Izabrani dezen'))

    class Meta:
        verbose_name = _('Stavka porudžbine')
        verbose_name_plural = _('Stavke porudžbine')

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    @property
    def subtotal(self):
        if self.quantity is not None and self.price is not None:
            return self.quantity * self.price
        return 0
