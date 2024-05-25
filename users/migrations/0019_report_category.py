# Generated by Django 4.2.10 on 2024-03-31 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_rename_in_progress_report_is_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='category',
            field=models.CharField(choices=[('general', 'General'), ('substance_abuse', 'Substance Abuse'), ('hazing_violation', 'Hazing Violation')], default='general', max_length=50),
        ),
    ]