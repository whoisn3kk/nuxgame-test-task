from decimal import Decimal
import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone

def get_future_date():
    return timezone.now() + timedelta(days=7)

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_future_date)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Token for {self.user.username}"

class GameResult(models.Model):
    class ResultChoice(models.TextChoices):
        WIN = 'win', 'Win'
        LOSE = 'lose', 'Lose'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_history')
    number = models.IntegerField()
    result = models.CharField(max_length=4, choices=ResultChoice.choices)
    prize = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.result} ({self.created_at.strftime('%Y-%m-%d')})"