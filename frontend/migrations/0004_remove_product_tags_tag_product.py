# Generated by Django 4.2.3 on 2023-07-18 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_tag_category_picture_product_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AddField(
            model_name='tag',
            name='product',
            field=models.ManyToManyField(to='frontend.product'),
        ),
    ]
