from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def index_api_view(request):
    return Response({"detail": "Application is running."})
