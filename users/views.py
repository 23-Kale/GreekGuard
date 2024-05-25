import os

import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout
from .models import Report, ReportForm, ExplanationForm
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    if(request.user.is_authenticated and request.user.username == 'admin'):
        logout(request)
    return render(request, "users/index.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def to_report(request):
    context = {}
    context['form'] = ReportForm()
    return render(request, "users/report.html", context)



def report_view(request): #edit of Heru's implementation to allow for Anonymous Users. -Ahbey
    if request.method == 'POST' : #necessary?
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid() :
            temp_report = form.save(commit=False)
            if request.user.is_authenticated:
                temp_report.user = request.user
            else:#if not authenticated
                #temp_report.user = Null
                temp_report.user = None
            temp_report.save()
            return render(request, 'users/reportsubmission.html')
    else:
        form = ReportForm()
    return render(request, 'users/report.html', {'form': form})

def explanation_view(request, report_id):
    if request.method == 'POST':
        form = ExplanationForm(request.POST)
        report = Report.objects.get(id = report_id)
        if form.is_valid():
            report.explanation_text = form.cleaned_data['explanation_text']
            report.save()
            return HttpResponseRedirect(reverse('users:report_details', args=(report_id,)))
    else:
        form = ExplanationForm()
    return HttpResponseRedirect(reverse('users:report_details', args=(report_id,)))


def view_reports(request):
    all_reports = Report.objects.all().order_by('-is_seen', '-is_resolved', '-id')
    return render(request, 'users/view_reports.html', {'all_reports': all_reports, 'current_user': request.user.id, 'isAdmin': is_admin(request.user)})

def change_report_seen(request, report_id):
    report = Report.objects.get(id = report_id)
    if not report.is_seen:
        report.is_seen = 1
        report.save()
    return HttpResponseRedirect(reverse('users:report_details', args=(report.id,)))

def change_report_resolved(request, report_id):
    report = Report.objects.get(id = report_id)
    if report.is_resolved:
        report.is_resolved = 0
        report.save()
    else:
        report.is_resolved = 1
        report.save()
    return HttpResponseRedirect(reverse('users:report_details', args = (report.id,)))

def change_report_status(request, report_id):
    report = Report.objects.get(id = report_id)
    if report.is_under_review:
        report.is_under_review = 0
    else:
        report.is_under_review = 1
    report.save()
    return HttpResponseRedirect(reverse('users:report_details', args=(report.id,)))

def report_details(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if report.file_upload == "":
        is_file = False
    else:
        is_file = True
    return render(request, 'users/report_detail.html', {'report': report, 'current_user': request.user.id, 'isAdmin': is_admin(request.user), 'form': ExplanationForm(), 'is_file': is_file})

def delete_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    report.file_upload.delete(save=False)
    report.delete()
    return HttpResponseRedirect(reverse('users:view_reports'))


def is_admin(user):
    return user.groups.filter(name='Site Admins').exists()
