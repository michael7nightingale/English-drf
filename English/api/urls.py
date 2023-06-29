from django.urls import path, include

from .docs import urlpatterns as docs_urlpatterns
from .views import IndexAPIView


urlpatterns = [
    path("docs/", include(docs_urlpatterns)),
    path('', IndexAPIView.as_view(), name='index'),
    path("categories/", include("words.urls")),
    path("auth/", include("users.urls")),
    path("messages/", include("chats.urls"))

]
