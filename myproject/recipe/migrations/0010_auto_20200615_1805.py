# Generated by Django 3.0.6 on 2020-06-15 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20200615_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
