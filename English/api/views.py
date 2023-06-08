from rest_framework import views, viewsets, generics, mixins
from rest_framework import authentication, permissions, status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model

from .models import Message
from .serializers import MessageSerializer
from ai.messenger import Messenger

from rest_framework.response import Response


User = get_user_model()


class IndexAPIView(views.APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "app started successfully"})


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_permissions(self):
        if self.action in ('send', "generate", None):
            permissions_classes = [permissions.IsAuthenticated]
        else:
            permissions_classes = [permissions.IsAdminUser]
        return [p() for p in permissions_classes]

    @action(methods=['post'], detail=False,
            url_path='send', url_name="send")
    def send(self, request):
        text = request.data.get('text')
        if text is None:
            return Response({"detail":  "text is not provided"})
        message = Message.objects.create(text=text, user=request.user)
        messenger = Messenger(message)
        messenger.chat()
        return Response({"detail": "message was sent"}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False,
            url_name="generate", url_path='generate')
    def generate(self, request):
        new_message = Messenger.generate()
        return Response({'message': self.serializer_class(new_message).data})

    @action(methods=['get'], detail=False,
            url_name='all', url_path='all')
    def all(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





