from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from ..models import Category, Issue


class CategoryTestCase(TestCase):
    """
    Test that categories can be created.
    This is assumed to work in Issue test, so it seems sensible to cover this by separate tests as well.
    """

    def setUp(self):
        Category.objects.create(title="Bug")

    def test_create_delete_category(self):
        bug = Category.objects.get(title="Bug")
        self.assertEqual(bug.title, "Bug")

    def test_duplicate_fails(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(title="Bug")


class IssueTestCase(TestCase):
    def setUp(self):
        """Create Users and Categories"""
        Category.objects.create(title="Bug")
        Category.objects.create(title="Feature")

        user_model = get_user_model()
        user_model.objects.create(username="test_user_a")
        user_model.objects.create(username="test_user_b")

    def create_issue(self, bug_category, reporter, assignee=None):
        return Issue.objects.create(
            title="Issue 1",
            description="Lorem Ipsum",
            category=bug_category,
            status=Issue.STATUS_TO_DO_NOW,
            reporter=reporter,
            assignee=assignee,
        )

    def test_create_basic(self):
        """Test that Issues can be created with just the necessary information"""
        bug_category = Category.objects.get(title="Bug")
        user = get_user_model().objects.first()

        # Create an issue
        self.create_issue(bug_category, user)

        # Check that it exists in the database
        issue = Issue.objects.get(title="Issue 1")

        # Test all fields
        self.assertEqual(issue.title, "Issue 1")
        self.assertEqual(issue.description, "Lorem Ipsum")
        self.assertEqual(issue.category, bug_category)
        self.assertEqual(issue.status, Issue.STATUS_TO_DO_NOW)
        self.assertEqual(issue.reporter, user)
        self.assertIsNone(issue.assignee)
        self.assertIsNone(issue.estimated_time)
        self.assertIsNone(issue.spent_time)

    def test_create_full(self):
        """Test that Issues can be created with all params available"""
        bug_category = Category.objects.get(title="Bug")

        first_user = get_user_model().objects.first()
        last_user = get_user_model().objects.last()

        Issue.objects.create(
            title="Issue 2",
            description="Lorem Ipsum",
            category=bug_category,
            status=Issue.STATUS_RESOLVED,
            reporter=first_user,
            assignee=last_user,
            estimated_time=timedelta(hours=2),
            spent_time=timedelta(hours=3),
        )

        issue = Issue.objects.get(title="Issue 2")
        # Test all fields
        self.assertEqual(issue.title, "Issue 2")
        self.assertEqual(issue.description, "Lorem Ipsum")
        self.assertEqual(issue.category, bug_category)
        self.assertEqual(issue.status, Issue.STATUS_RESOLVED)
        self.assertEqual(issue.reporter, first_user)
        self.assertEqual(issue.assignee, last_user)
        self.assertEqual(issue.estimated_time, timedelta(hours=2))
        self.assertEqual(issue.spent_time, timedelta(hours=3))

    def test_edit(self):
        bug_category = Category.objects.get(title="Bug")
        user = get_user_model().objects.first()

        self.create_issue(bug_category, user)
        issue = Issue.objects.get(title="Issue 1")

        # Rename
        issue.title = "Issue 3"
        issue.save()

        # Check that it exists in the database
        issue = Issue.objects.get(title="Issue 3")

        self.assertEqual(issue.title, "Issue 3")

    def test_delete(self):
        bug_category = Category.objects.get(title="Bug")
        user = get_user_model().objects.first()

        # Create an issue
        issue = self.create_issue(bug_category, user)
        # Delete it
        issue.delete()

        with self.assertRaises(Issue.DoesNotExist):
            # Try to get it once again after it has been deleted
            Issue.objects.get(title="Issue 1")
