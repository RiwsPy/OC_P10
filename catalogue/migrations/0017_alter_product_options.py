# Generated by Django 3.2.8 on 2021-10-26 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0016_alter_favorite_product_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['code'], 'verbose_name': 'produit'},
        ),
    ]