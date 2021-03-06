# Generated by Django 3.2.9 on 2021-11-23 12:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_products_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='date_product',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='products',
            name='product_owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
