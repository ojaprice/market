# Generated by Django 4.2.16 on 2024-10-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_remove_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="store"),
        ),
    ]
