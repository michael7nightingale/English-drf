from rest_framework import views, viewsets, generics
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from . import models


class IndexAPIView(views.APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        print(123123)
        return Response({"detail": "app started successfully"})



