from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view),
    path("report", views.to_report, name="to_report"),
    path("reportsubmission", views.report_view, name="report_view"),
    path("view_reports", views.view_reports, name="view_reports"),
    path("<int:report_id>/explanation_view", views.explanation_view, name="explanation_view"),
    path("<int:report_id>/change_report_status", views.change_report_status, name="change_report_status"),
    path("<int:report_id>/change_report_seen", views.change_report_seen, name = "change_report_seen"),
    path("<int:report_id>/change_report_resolved", views.change_report_resolved, name = "change_report_resolved"),
    path("<int:report_id>/report_details", views.report_details, name="report_details"),
    path("<int:report_id>/delete_report", views.delete_report, name="delete_report")
]