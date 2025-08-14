from rest_framework import serializers
from .models import User, AuthToken, GameResult

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ['token', 'expires_at']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'created_at']

class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ['number', 'result', 'prize', 'created_at']