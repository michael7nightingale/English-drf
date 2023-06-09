from rest_framework import viewsets, mixins, permissions, generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from http import HTTPStatus

from .models import Account, User
from .serializers import AccountCreateSerializer, AccountDetailSerializer, UserCreateSerializer
from .service.email import check_activation_token, decode_uid, send_email


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
        send_email(
            request=request,
            user=new_account.user,
            user_email=new_account.user.email
        )
        message = (
            f"{new_account.user.username}! Please, check your email {new_account.user.email} and follow the link"
            "in the message we have send you to finish the registration."
        )
        return Response(message, status=HTTPStatus.CREATED)

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


class AccountDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    lookup_url_kwarg = "username"
    lookup_field = "user__username"


@api_view(['get'])
def activate_user(request, uid: str, token: str):
    try:
        user = User.objects.get(pk=decode_uid(uid))
    except ():
        user = None

    if user is not None and check_activation_token(user=user, token=token):
        user.is_active = True
        user.save()
        return Response("Registration is finished successfully.", status=HTTPStatus.OK)
    else:
        return Response("Activation link is invalid.", status=HTTPStatus.BAD_REQUEST)
