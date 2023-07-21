# Generated by Django 4.2.3 on 2023-07-21 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0006_userprofile_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='frontend.userprofile'),
        ),
    ]
