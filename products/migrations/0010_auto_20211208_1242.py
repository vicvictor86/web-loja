# Generated by Django 3.2.9 on 2021-12-08 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_products_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='comment1',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='comment2',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_informations',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_resume',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='reasons_to_buy',
            field=models.CharField(max_length=1000),
        ),
    ]
