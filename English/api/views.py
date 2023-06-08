from django.forms import model_to_dict
from rest_framework import views, viewsets, generics, mixins
from rest_framework import authentication, permissions, status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import Message, Category, Word
from .paginators import MessagesListPaginator
from .serializers import MessageSerializer, CategorySerializer, WordSerializer
from ai.messenger import Messenger


User = get_user_model()


class IndexAPIView(views.APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "app started successfully"})


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    pagination_class = MessagesListPaginator

    def get_permissions(self):
        if self.action in ('send', "generate", None):
            permissions_classes = [permissions.IsAuthenticated]
        else:
            permissions_classes = [permissions.IsAdminUser]
        return [p() for p in permissions_classes]

    @action(methods=['post'], detail=False,
            url_path='send', url_name="send")
    def send(self, request):
        data = {
            "text": request.data.get("text"),
            "type": request.data.get("type"),
            "reply_to": request.data.get("reply_to"),
            "user": request.user
        }
        print(data)
        if data['reply_to']:
            try:
                message_to_reply = Message.objects.get(id=int(data['reply_to']))
                data['reply_to'] = message_to_reply
                message_type = message_to_reply.type
                if data['type'] != "pupil":
                    return Response({"detail": "Unexpected mode"})
                else:
                    if message_type != data['type']:
                        return Response({"detail": "Not right message to reply"})
            except:
                return Response({"detail": "Message to reply is not found"})
        else:
            data["reply_to"] = None
        if data['text'] is None:
            return Response({"detail":  "text is not provided"})
        message = Message.objects.create(**data)
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


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        data = self.queryset.values()
        for q, d in zip(self.queryset.all(), data):
            d['url'] = q.get_absolute_url()
            d['count'] = q.count()
        serializer = self.serializer_class(data=list(data), many=True)
        serializer.is_valid(raise_exception=True)
        return Response({"categories": serializer.validated_data})


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        category_name = kwargs.get('category_name')
        if category_name is None:
            return Response({"detail": "missing category name"})
        try:

            instance = Category.objects.get(title=category_name)
            data = model_to_dict(instance)
            data['count'] = instance.count()
            serializer = self.serializer_class(data=data, many=False)
            serializer.is_valid(raise_exception=True)
            return Response({'category': serializer.validated_data})

        except Exception as e:
            print(e)
            return Response({"detail": "category is not found"})


class WordsListAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def list(self, request, *args, **kwargs):
        category_name = kwargs.get("category_name")
        if category_name is None:
            return Response({"detail": "category name is required"})

        words = self.queryset.filter(category__title=category_name)
        serializer = self.serializer_class(instance=words, many=True)
        return Response({"words": serializer.data})
