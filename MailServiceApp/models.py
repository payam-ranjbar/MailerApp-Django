from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from Mailer import settings


class Mail(models.Model):
    subject = models.CharField(max_length=100)
    text = models.TextField()
    attachment = models.FileField()



class Account(AbstractUser):
    friends = models.ManyToManyField('self')


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Recipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


