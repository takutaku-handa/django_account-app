# Generated by Django 3.0.6 on 2020-05-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200523_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='checkedfood',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='checkweight',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='foodname',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='foodweight',
        ),
        migrations.AddField(
            model_name='profile',
            name='foodname1',
            field=models.CharField(default='', max_length=10),
        ),
    ]
