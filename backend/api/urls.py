from django.urls import path
from api.views import *

urlpatterns = [
    path('user/register', UserRegisterView.as_view(), name='user-register'),
    path('game/<uuid:token>', UserInfoView.as_view(), name='user-info'),
    path('game/<uuid:token>/renew', RenewTokenView.as_view(), name='token-renew'),
    path('game/<uuid:token>/deactivate', DeactivateTokenView.as_view(), name='token-deactivate'),
    path('game/<uuid:token>/play', PlayGameView.as_view(), name='game-play'),
    path('game/<uuid:token>/history', GameHistoryView.as_view(), name='game-history'),
]