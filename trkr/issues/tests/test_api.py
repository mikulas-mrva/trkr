from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    force_authenticate,
    APIRequestFactory,
    APITestCase,
    APIClient,
)

from ..models import Issue
from ..views import IssueViewSet


class IssueTests(APITestCase):
    fixtures = ["test_data.json"]

    issue_data = {
        "title": "Issue 1",
        "description": "lorem ipsum",
        "category": "Bug",
        "status": "In Progress",
        "reporter": "superuser",
        "assignee": "staff_user",
        "estimated_time": "2 02:00:00",
        "spent_time": "01:30:00",
    }

    def test_create_superuser(self):
        """A superuser can create a new issue"""
        # Create a post request
        url = reverse("issue-list")
        factory = APIRequestFactory()
        superuser = get_user_model().objects.get(username="superuser")

        request = factory.post(url, self.issue_data, format="json")
        force_authenticate(request, user=superuser)

        # count issues before request for easy comparison
        issue_count = Issue.objects.count()
        response = IssueViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # One more issue was created
        self.assertEqual(Issue.objects.count(), issue_count + 1)

        # Check all data
        issue = Issue.objects.last()
        self.assertEqual(issue.title, "Issue 1")
        self.assertEqual(issue.description, "lorem ipsum")
        self.assertEqual(issue.category.title, "Bug")
        self.assertEqual(issue.status, Issue.STATUS_IN_PROGRESS)
        self.assertEqual(issue.reporter.username, "superuser")
        self.assertEqual(issue.assignee.username, "staff_user")
        self.assertEqual(issue.estimated_time, timedelta(days=2, hours=2))
        self.assertEqual(issue.spent_time, timedelta(hours=1, minutes=30))

    def test_create_staff_user(self):
        """A staff user cannot create issues by default"""
        url = reverse("issue-list")
        staff_user = get_user_model().objects.get(username="staff_user")

        # Create a post request
        factory = APIRequestFactory()
        request = factory.post(url, self.issue_data, format="json")
        force_authenticate(request, user=staff_user)

        response = IssueViewSet.as_view({"post": "create"})(request)
        # 403 Access Forbidden
        self.assertEqual(response.status_code, 403)

    def test_get_issue(self):
        """A staff user can read issues"""
        # Get issue from fixtures
        issue = Issue.objects.first()

        # Log in as staff_user
        client = APIClient()
        client.login(username="staff_user", password="staff_password")

        response = client.get(
            reverse("issue-detail", kwargs={"pk": issue.pk}), format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("title"), "Fixture Issue")

        client.logout()
