# Generated by Django 4.2.10 on 2024-03-14 18:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_report_file_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date_reported',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date reported'),
        ),
    ]
