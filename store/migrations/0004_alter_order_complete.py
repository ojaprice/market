# Generated by Django 4.2.16 on 2024-10-16 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="complete",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
