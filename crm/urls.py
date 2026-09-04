from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


def root_redirect(request):
    return redirect("login")


urlpatterns = [
    path("", root_redirect),
    path("crm/", include("user.urls")),
    path("admin/", admin.site.urls),
]
