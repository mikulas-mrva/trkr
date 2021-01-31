from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from trkr.issues import views

router = routers.DefaultRouter()
router.register(r"issues", views.IssueViewSet)

urlpatterns = [
    path("api/v1/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include(router.urls)),
    path("", admin.site.urls),
]
