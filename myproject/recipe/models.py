from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django_mysql.models import ListCharField


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pub = models.BooleanField(default=False)
    name = models.CharField(max_length=50, unique=True, null=True)
    ingredient = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20 * 11,
        null=True,
    )
    weight = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20 * 11,
        null=True,
    )
    hyojiweight = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20 * 11,
        null=True,
    )
    hyojiryo = ListCharField(
        base_field=CharField(max_length=10, null=True),
        size=20,
        max_length=20 * 11,
        null=True,
    )

    recipe = models.TextField(max_length=8000, null=True, blank=True)

    def __str__(self):
        return self.name


class MyCalender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    time = models.IntegerField(choices=((1, '朝'), (2, '昼'), (3, '夜'), (4, '間食等')), null=True)
    name = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    ryo = models.FloatField(choices=((0.5, '半分'), (0.75, '少なめ'), (1.0, '普通'),
                                     (1.25, '少し多め'), (1.5, '多め'), (2.0, '二人前')), default=1.0)

    def __str__(self):
        return str(self.user) + str(self.date) + str(self.time) + str(self.name)
