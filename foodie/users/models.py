import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from datetime import datetime

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True)
    avatar = models.ImageField(null=True)
    is_premium = models.BooleanField(default=False)
    reputation = models.FloatField(default=2.5)
    is_delivery = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True, blank=True)
    location_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['date_joined']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
