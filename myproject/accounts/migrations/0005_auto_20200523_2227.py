# Generated by Django 3.0.6 on 2020-05-23 13:27

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200523_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foodname',
            field=django_mysql.models.ListCharField(models.CharField(max_length=10, null=True), max_length=220, null=True, size=20),
        ),
    ]