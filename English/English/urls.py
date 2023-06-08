from django.urls import path, include
from django.shortcuts import redirect
from django.contrib import admin

from .docs import urlpatterns as docs_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", lambda request: redirect("api/v1/")),
    path(r'docs/', include(docs_urlpatterns)),
    path(r"api/v1/", include("api.urls")),
    path(r"api/v1/", include("users.urls")),

]
