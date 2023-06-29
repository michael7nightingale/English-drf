from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Account
from .serializers import AccountCreateSerializer, AccountDetailSerializer, UserCreateSerializer


class AccountViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = AccountCreateSerializer
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.action in ('me', "update", "delete"):
            permissions_classes = [permissions.IsAuthenticated]
        else:
            permissions_classes = [permissions.AllowAny]
        return [permission() for permission in permissions_classes]

    def create(self, request, *args, **kwargs):
        """Create both user and account."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_account = Account.objects.create_account(**request.data)
        return Response(AccountDetailSerializer(new_account).data, status=201)

    @action(methods=['get'], detail=False)
    def me(self, request):
        account = request.user.account
        serializer = AccountDetailSerializer(instance=account)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update account or account and user together. Data is given
        as on account creation, but partial.
        """
        data = dict(**request.data)
        if "user" in data:
            user_serializer = UserCreateSerializer(instance=request.user, data=data['user'], partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.update(request.user, user_serializer.validated_data)
            data.pop('user')

        serializer = self.serializer_class(instance=request.user.account, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.account, serializer.validated_data)
        return Response(serializer.validated_data)
