from django.urls import path, include
from django.contrib import admin

from .docs import urlpatterns as docs_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'docs/', include(docs_urlpatterns)),
    path(r"api/v1/", include("api.urls")),


]
