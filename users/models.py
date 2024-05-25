import os.path
from django.utils import timezone

import boto3
from django.contrib.auth.models import User
from django.db import models
from storages.backends import s3boto3
from django.forms import ModelForm, ClearableFileInput
from django import forms


# Create your models here.

class Report(models.Model):
    file_upload = models.FileField(null=True, blank=True, default=None, upload_to='uploads/',
                                   storage=s3boto3.S3StaticStorage())
    submission_text = models.CharField(max_length=200, null=True, blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    date_reported = models.DateTimeField("date reported", default=timezone.now)
    is_seen = models.BooleanField(default=None, null=True, blank=True) #Changed from "is_under_review" to "is_seen"
    is_resolved = models.BooleanField(default=None, null=True, blank=True) #Added a secondary boolean for the "resolved" status
    explanation_text = models.CharField(max_length=200, null=True, blank=True, default="") #Added an explanation text field in case admins want to explain
    category = models.CharField(max_length=50, choices=(
        ('general', 'General'),
        ('substance_abuse', 'Substance Abuse'),
        ('hazing_violation', 'Hazing Violation')
    ), default='general')

    def __str__(self):
        if self.submission_text:
            return self.submission_text
        return "No Report Text"



class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['submission_text', 'file_upload', 'category']
        widgets = {
            'file_upload': ClearableFileInput(attrs={
                'accept': '.pdf, .jpg, .jpeg, .png'  # accept only PDF, JPG/JPEG, and PNG files.
            }) ,
        }

class ExplanationForm(ModelForm):
    class Meta:
        model = Report
        fields = ['explanation_text']
