import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_mysql.models import ListCharField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    foodname = ListCharField(
        base_field=CharField(max_length=10, null=True, blank=True),
        size=21,
        max_length=21 * 11,
        null=True,
        blank=True
    )

    foodweight = ListCharField(
        base_field=CharField(max_length=10, null=True, blank=True),
        size=21,
        max_length=21 * 11,
        null=True,
        blank=True
    )

    checkedfood = ListCharField(
        base_field=CharField(max_length=10, null=True, blank=True),
        size=21,
        max_length=21 * 11,
        null=True,
        blank=True
    )

    checkweight = ListCharField(
        base_field=CharField(max_length=10, null=True, blank=True),
        size=21,
        max_length=21 * 11,
        null=True,
        blank=True
    )

    checkryo = ListCharField(
        base_field=CharField(max_length=10, null=True, blank=True, default="g"),
        size=21,
        max_length=21 * 11,
        null=True,
        blank=True
    )

    day = models.DateField(default=datetime.date.today())



    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

