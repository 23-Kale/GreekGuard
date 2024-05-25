from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test.client import Client
from .models import Report, ReportForm
from django.utils import timezone, dateformat

import random

def get_random_string():
    r = ''
    chars = 'qwertyuiopasdfghjklzxcvbnm123467890QWERTYUIOPASDFGHJKLZXVNM'
    for i in range(8):
        r += random.choice(chars)
    return r

class HomeIndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345", first_name = "John", last_name = "Doe", email="testuser@example.com")
        group, created = Group.objects.get_or_create(name="Site Admins")
        self.user.groups.add(group)
        self.client = Client()
        self.client.login(username="testuser", password="12345")
    
    def test_root_status_ok(self):
        response = self.client.get(reverse("users:index"))
        self.assertEqual(response.status_code, 200)

    def test_root_displays_full_name(self):
        response = self.client.get(reverse("users:index"))
        self.assertContains(response, "Name: John Doe")

    def test_root_displays_email(self):
        response = self.client.get(reverse("users:index"))
        self.assertContains(response, "You are signed in as: testuser@example.com")

    def test_root_displays_site_admin(self):
        response = self.client.get(reverse("users:index"))
        self.assertContains(response, "Welcome, Site Admin!")

class ViewReportsTest(TestCase):
    def setUp(self):
        self.site_admin = User.objects.create_user(username="testuser", password="12345", first_name = "John", last_name = "Doe", email="testuser@example.com")
        self.standard = User.objects.create_user(username="standarduser", password="12345", first_name = "John", last_name = "Doe", email="standarduser@example.com")
        site_admin_group, created = Group.objects.get_or_create(name="Site Admins")
        self.site_admin.groups.add(site_admin_group)
        self.client = Client()

    def test_page_status_ok(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:view_reports"))
        self.assertEqual(response.status_code, 200)

    def test_user_sees_own_report(self):
        r = get_random_string()
        report = Report.objects.create(user=self.site_admin, submission_text=r, is_seen=False, is_resolved=False)
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:view_reports"))
        # expected = '<tr>\n      <td>1</td>\n      <td>THIS IS A TEST</td>\n      <td>' + dateformat.format(timezone.now(), 'N j, Y, P') + '</td>\n    <td>general</td>\n      <td>\n        \n          New\n        \n      </td>\n      <td><a href="/1/change_report_seen" class="btn btn-info btn-sm">Report Link</a></td>\n    </tr>'
        self.assertContains(response, r)

    def test_standard_user_does_not_see_admin_test(self):
        r = get_random_string()
        report = Report.objects.create(user=self.site_admin, submission_text=r, is_seen=False, is_resolved=False)
        self.client.login(username="standarduser", password="12345")
        response = self.client.get(reverse("users:view_reports"))
        # expected = '<tr>\n      <td>1</td>\n      <td>THIS IS A TEST</td>\n      <td>' + dateformat.format(timezone.now(), 'N j, Y, P') + '</td>\n    <td>general</td>\n      <td>\n        \n          New\n        \n      </td>\n      <td><a href="/1/change_report_seen" class="btn btn-info btn-sm">Report Link</a></td>\n    </tr>'
        self.assertNotContains(response, r)

    def test_admin_sees_standard_and_admin_tests(self):
        r1 = get_random_string()
        r2 = get_random_string()
        report = Report.objects.create(user=self.site_admin, submission_text=r1, is_seen=False, is_resolved=False)
        report = Report.objects.create(user=self.standard, submission_text=r2, is_seen=False, is_resolved=False)
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:view_reports"))
        expected_admin = '<tr>\n      <td>1</td>\n      <td>THIS IS A REPORT BY AN ADMIN</td>\n      <td>' + dateformat.format(timezone.now(), 'N j, Y, P') + '</td>\n    <td>general</td>\n      <td>\n        \n          New\n        \n      </td>\n      <td><a href="/1/change_report_seen" class="btn btn-info btn-sm">Report Link</a></td>\n    </tr>'
        expected_standard = '<tr>\n      <td>2</td>\n      <td>THIS IS A REPORT BY A STANDARD USER</td>\n      <td>' + dateformat.format(timezone.now(), 'N j, Y, P') + '</td>\n    <td>general</td>\n      <td>\n        \n          New\n        \n      </td>\n      <td><a href="/2/change_report_seen" class="btn btn-info btn-sm">Report Link</a></td>\n    </tr>'
        self.assertContains(response, r1)
        self.assertContains(response, r2)

    def test_different_category(self):
        r = get_random_string()
        report = Report.objects.create(user=self.site_admin, submission_text=r, is_seen=False, is_resolved=False, category='substance_abuse')
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:view_reports"))
        expected = '<tr>\n      <td>1</td>\n      <td>THIS IS A TEST</td>\n      <td>' + dateformat.format(timezone.now(), 'N j, Y, P') + '</td>\n    <td>substance_abuse</td>\n      <td>\n        \n          New\n        \n      </td>\n      <td><a href="/1/change_report_seen" class="btn btn-info btn-sm">Report Link</a></td>\n    </tr>'
        self.assertContains(response, r)

class ReportsDetailTest(TestCase):
    def setUp(self):
        self.site_admin = User.objects.create_user(username="testuser", password="12345", first_name = "John", last_name = "Doe", email="testuser@example.com")
        self.standard = User.objects.create_user(username="standarduser", password="12345", first_name = "John", last_name = "Doe", email="standarduser@example.com")
        site_admin_group, created = Group.objects.get_or_create(name="Site Admins")
        self.site_admin.groups.add(site_admin_group)
        self.r1 = get_random_string()
        self.r2 = get_random_string
        self.site_admin_report = Report.objects.create(user=self.site_admin, submission_text=self.r1, is_seen=False, is_resolved=False)
        self.standard_user_report = Report.objects.create(user=self.standard, submission_text=self.r2, is_seen=False, is_resolved=False)
        self.client = Client()

    def test_page_status_ok(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_can_modify_own_test(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 1}))
        expected = '<a href="#" class="btn btn-danger mt-3 mb-2" data-bs-toggle="modal" data-bs-target="#deleteConfirmation">Delete Report?</a>'
        # expected = '<a href="/1/delete_report" class="btn btn-danger mt-3">Delete Report?</a>'
        self.assertContains(response, expected)

    def test_cannot_modify_other_user_test(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 2}))
        expected = '<a href="#" class="btn btn-danger mt-3 mb-2" data-bs-toggle="modal" data-bs-target="#deleteConfirmation">Delete Report?</a>'
        self.assertNotContains(response, expected)

    def test_can_view_proper_report(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 1}))
        self.assertContains(response, self.r1)

    def test_cannot_resolve_report_as_standard_user(self):
        self.client.login(username="standarduser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 2}))
        expected = '<a href="/2/change_report_resolved" class="btn btn-info mt-3 mb-2">Mark as resolved</a>'
        self.assertNotContains(response, expected)

    def test_admin_can_reopen_resolved_report(self):
        resolved_report = Report.objects.create(user=self.site_admin, submission_text=self.r1, is_seen=True, is_resolved=True)
        self.client = Client()
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 3}))
        expected = '<a href="/3/change_report_resolved" class="btn btn-info mt-3 mb-2">Re-Open Report?</a>'
        self.assertContains(response, expected)

    def test_standard_user_cannot_reopen_resolved_report(self):
        resolved_report = Report.objects.create(user=self.standard, submission_text=self.r1, is_seen=True, is_resolved=True)
        self.client = Client()
        self.client.login(username="standarduser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 3}))
        expected = '<a href="/3/change_report_resolved" class="btn btn-info mt-3 mb-2">Re-Open Report?</a>'
        self.assertNotContains(response, expected)

    def test_standard_user_cannot_change_explanation_text(self):
        resolved_report = Report.objects.create(user=self.standard, submission_text=self.r1, is_seen=True, is_resolved=False)
        self.client = Client()
        self.client.login(username="standarduser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 3}))
        expected = '<button type="submit" class="btn btn-success">Change Explanation</button>'
        self.assertNotContains(response, expected)

    def test_standard_user_can_see_explanation_text(self):
        explanation = get_random_string()
        resolved_report = Report.objects.create(user=self.standard, submission_text=self.r1, is_seen=True, is_resolved=True, explanation_text=explanation)
        self.client = Client()
        self.client.login(username="standarduser", password="12345")
        response = self.client.get(reverse("users:report_details", kwargs={'report_id': 3}))
        self.assertContains(response, explanation)

class ReportFormTest(TestCase):
    def setUp(self):
        self.site_admin = User.objects.create_user(username="testuser", password="12345", first_name = "John", last_name = "Doe", email="testuser@example.com")
        self.form_data = {
            'submission_text': get_random_string(),
            'user': self.site_admin,
            'category': 'general'
        }
        
    def test_form_is_valid(self):
        form = ReportForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_needs_category(self):
        form = ReportForm({})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors, {
            'category': ['This field is required.']
        })

    def test_anonymous_user_can_submit_form(self):
        self.form_data = {
            'submission_text': get_random_string(),
            'category': 'general'
        }
        form = ReportForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_different_category(self):
        self.form_data = {
            'submission_text': get_random_string(),
            'category': 'substance_abuse'
        }
        form = ReportForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['category'], self.form_data['category'])