# Generated by Django 3.2.5 on 2021-08-08 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_rename_c_name_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(
                max_length=13,
                primary_key=True,
                serialize=False),
        ),
    ]
