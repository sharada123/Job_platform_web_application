# Generated by Django 5.1 on 2025-02-28 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='logo',
            field=models.ImageField(blank=True, upload_to='logo/'),
        ),
        migrations.AddField(
            model_name='job',
            name='required_education',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
