import re
from django.http import JsonResponse
from django.utils import timezone
from .models import AuthToken


PROTECTED_PATHS_PATTERNS = [
    re.compile(r'^/game/(?P<token>[a-fA-F0-9-]+)$'),         # /game/{token}
    re.compile(r'^/game/(?P<token>[a-fA-F0-9-]+)/renew$'),    # /game/{token}/renew
    re.compile(r'^/game/(?P<token>[a-fA-F0-9-]+)/deactivate$'),# /game/{token}/deactivate
    re.compile(r'^/game/(?P<token>[a-fA-F0-9-]+)/play$'),     # /game/{token}/play
    re.compile(r'^/game/(?P<token>[a-fA-F0-9-]+)/history$'),  # /game/{token}/history
]

class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        token_value = None
        
        for pattern in PROTECTED_PATHS_PATTERNS:
            match = pattern.match(path)
            if match:
                token_value = match.group('token')
                break
        
        if not token_value:
            return self.get_response(request)

        try:
            token = AuthToken.objects.select_related('user').get(pk=token_value)
        except (AuthToken.DoesNotExist, ValueError):
            return JsonResponse({"error": "Invalid token"}, status=401)

        if not token.is_active:
            return JsonResponse({"error": "Token is deactivated"}, status=403)

        if token.expires_at < timezone.now():
            token.is_active = False
            token.save()
            return JsonResponse({"error": "Token has expired"}, status=403)
        
        request.game_user = token.user
        request.auth_token = token
        
        return self.get_response(request)