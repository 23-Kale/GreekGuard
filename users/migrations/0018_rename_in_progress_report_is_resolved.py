# Generated by Django 4.2.10 on 2024-03-29 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_report_explanation_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='in_progress',
            new_name='is_resolved',
        ),
    ]