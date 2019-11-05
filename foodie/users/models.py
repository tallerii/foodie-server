import uuid
from django.contrib.gis.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, default=True)
    is_delivery = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    reputation = models.FloatField(default=2.5)
    last_location = models.PointField(default=None, null=True)
    location_last_updated = models.DateTimeField(auto_now_add=True)
    FCMToken = models.CharField(max_length=300)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['date_joined']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
