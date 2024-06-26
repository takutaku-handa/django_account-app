# Generated by Django 3.0.6 on 2020-06-12 12:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0004_auto_20200610_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCalender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2020, 6, 12), null=True)),
                ('time', models.IntegerField(choices=[(1, '朝'), (2, '昼'), (3, '夜'), (4, '間食等')], default=2, null=True)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.Recipe')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
