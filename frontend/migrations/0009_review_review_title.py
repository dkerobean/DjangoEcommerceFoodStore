# Generated by Django 4.2.3 on 2023-07-26 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
