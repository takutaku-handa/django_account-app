# Generated by Django 3.0.6 on 2020-06-16 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_mycalender_ryo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycalender',
            name='ryo',
            field=models.FloatField(choices=[(0.5, '半分'), (0.75, '少なめ'), (1.0, '普通'), (1.25, '少し多め'), (1.5, '多め'), (2.0, '二人前')], default=1.0),
        ),
    ]