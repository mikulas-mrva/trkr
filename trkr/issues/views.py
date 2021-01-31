from rest_framework import permissions, viewsets

from .models import Issue
from .serializers import IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    Issue API endpoint
    """

    queryset = Issue.objects.all().order_by("-modified_at")
    serializer_class = IssueSerializer
    permission_classes = [permissions.DjangoModelPermissions]
