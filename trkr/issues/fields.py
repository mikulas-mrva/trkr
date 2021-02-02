from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRelatedAPIField(serializers.RelatedField):
    """Serializer field that displays usernames instead of user pks"""

    queryset = get_user_model().objects.all()

    def to_representation(self, obj):
        return obj.username

    def to_internal_value(self, value):
        return self.queryset.get(username=value)


class IssueStatusChoiceField(serializers.ChoiceField):
    """Serializer field that displays full name of issues status instead of one character code"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse_choices = {name: code for (code, name) in self.choices.items()}

    def to_representation(self, value):
        return self.choices.get(value)

    def to_internal_value(self, value):
        return self.reverse_choices.get(value)
