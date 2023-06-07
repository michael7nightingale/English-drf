from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        if self.action in ('list', 'delete'):
            permissions_classes = [permissions.IsAdminUser]
        elif self.action in ('retrieve', ):
            permissions_classes = [permissions.IsAuthenticated]
        else:
            permissions_classes = [permissions.AllowAny]
        return [permission() for permission in permissions_classes]

    def list(self, request, *args, **kwargs):
        return Response({"users": self.serializer_class(self.get_queryset(), many=True).data})

    @action(methods=['POST'], detail=False,
            url_name='users_login', url_path='login')
    def login_user(self, request, *args, **kwargs):
        user = User.login(**request.data)
        if user is None:
            return Response({"detail": "No data supplied"})
        login(request, user)
        return Response({"user": self.serializer_class(user).data})

    @action(methods=['POST'], detail=False,
            url_name='users_register', url_path='register')
    def register_user(self, request):
        user = User.register(**request.data)
        if user is None:
            return Response(status=400, data={"detail": "Invalid data."})

        ser = self.serializer_class(instance=user)
        login(request, user)
        return Response({"user": ser.data})

    @action(methods=['POST'], detail=False,
            url_name='users_logout', url_path='logout')
    def logout_user(self, request):
        logout(request)
        return redirect(reverse('index'))

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('pk')
        user = User.objects.get(username=username)
        ser = self.serializer_class(user)
        return Response({"user": ser.data})


