# Generated by Django 3.0.6 on 2020-06-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_recipe_hyojiryo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe',
            field=models.TextField(blank=True, max_length=8000, null=True),
        ),
    ]
