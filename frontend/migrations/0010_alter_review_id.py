# Generated by Django 4.2.3 on 2023-07-27 12:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0009_review_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
