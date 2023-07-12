from django.urls import path, include

from .docs import urlpatterns as docs_urlpatterns
from .views import index_api_view


urlpatterns = [
    path("docs/", include(docs_urlpatterns)),
    path('', index_api_view, name='index'),
    path("categories/", include("words.urls")),
    path("auth/", include("users.urls")),
    path("chats/", include("chats.urls")),

]
