from rest_framework import serializers

from .models import Account, User


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, allow_null=False)
    last_name = serializers.CharField(max_length=30, allow_null=False)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class AccountCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Account
        fields = ("user", 'location')


class AccountDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', "email"
                  'location', "get_avatar_url", "score", "level")


class AccountShortDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="account.user.username")

    class Meta:
        model = Account
        fields = ("username", )
