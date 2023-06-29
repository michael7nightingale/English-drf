from rest_framework import views
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
import logging


logger = logging.getLogger(__name__)
User = get_user_model()


class IndexAPIView(views.APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "app started successfully"})
