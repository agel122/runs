from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Run


class RunSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(source="owner_id", required=False)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

