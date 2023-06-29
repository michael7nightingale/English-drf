from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from rest_framework import permissions


schema_view = get_schema_view(
    info=openapi.Info(
        title="API English",
        default_version='v1.0',
        description='',
        license=openapi.License("License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    re_path(r'swagger/(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='swagger_format'),
    path(r"swagger/", schema_view.with_ui("swagger", cache_timeout=0), name='swagger'),
    path(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name='redoc')
]
