# Generated by Django 4.2.10 on 2024-03-13 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_report_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file_upload',
            field=models.FileField(default=None, upload_to='uploads/'),
        ),
    ]
