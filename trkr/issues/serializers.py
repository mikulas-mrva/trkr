from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import IssueStatusChoiceField, UserRelatedAPIField
from .models import Category, Issue


class IssueSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    status = IssueStatusChoiceField(Issue.STATUS_CHOICES)

    reporter = UserRelatedAPIField(
        required=False, default=serializers.CurrentUserDefault()
    )
    assignee = UserRelatedAPIField(required=False)

    estimated_time = serializers.DurationField(required=False)
    spent_time = serializers.DurationField(required=False)

    class Meta:
        model = Issue
        fields = "__all__"
