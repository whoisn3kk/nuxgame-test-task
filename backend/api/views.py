from django.shortcuts import render

# Create your views here.
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AuthToken, GameResult
from .serializers import *

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AuthToken.objects.create(user=user)
            token_serializer = TokenSerializer(token)
            return Response({
                "user_id": user.id, #type: ignore
                **token_serializer.data #type: ignore
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserInfoSerializer(request.game_user)
        return Response(serializer.data)

class RenewTokenView(APIView):
    def post(self, request, *args, **kwargs):
        # Деактивуємо старий токен
        old_token = request.auth_token
        old_token.is_active = False
        old_token.save()

        # Створюємо новий
        new_token = AuthToken.objects.create(user=request.game_user)
        serializer = TokenSerializer(new_token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeactivateTokenView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.auth_token
        token.is_active = False
        token.save()
        return Response({"message": "Token deactivated successfully"}, status=status.HTTP_200_OK)

class PlayGameView(APIView):
    def post(self, request, *args, **kwargs):
        random_number = random.randint(1, 1000)
        prize = 0.0

        if random_number % 2 == 0:
            result = 'win'
            if random_number > 900:
                prize = random_number * 0.7
            elif random_number > 600:
                prize = random_number * 0.5
            elif random_number > 300:
                prize = random_number * 0.3
            else:
                prize = random_number * 0.1
        else:
            result = 'lose'

        GameResult.objects.create(
            user=request.game_user,
            number=random_number,
            result=result,
            prize=round(prize, 2)
        )

        return Response({
            "random_number": random_number,
            "result": result,
            "prize": round(prize, 2)
        })

class GameHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        history = request.game_user.game_history.order_by('-created_at')[:3]
        serializer = GameResultSerializer(history, many=True)
        return Response(serializer.data)