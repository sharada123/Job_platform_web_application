# Generated by Django 5.1 on 2025-02-28 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_job_required_education'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='posted_by',
        ),
    ]
