# Generated by Django 3.0.6 on 2020-06-13 03:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_mycalender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycalender',
            name='date',
            field=models.DateField(default=datetime.date(2020, 6, 13), null=True),
        ),
    ]
