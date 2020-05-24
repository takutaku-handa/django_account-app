from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_mysql.models import ListCharField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    foodname = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20*11,
        null=True,
    )

    foodweight = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20*11,
        null=True,
    )

    checkedfood = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20*11,
        null=True,
    )

    checkweight = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20*11,
        null=True,
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
