from django.urls import path, include

from .views import *
from .serializers import *


urlpatterns = [
    path('', IndexAPIView.as_view(), name='index'),

]

