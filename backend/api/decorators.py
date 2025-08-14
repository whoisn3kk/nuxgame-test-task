from functools import wraps
from django.http import JsonResponse
from django.utils import timezone
from .models import AuthToken

def validate_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token_value = kwargs.get("token")
        if not token_value:
            return JsonResponse({"error": "Token not provided"}, status=401)

        try:
            token = AuthToken.objects.select_related('user').get(pk=token_value)
        except AuthToken.DoesNotExist:
            return JsonResponse({"error": "Invalid token"}, status=401)

        if not token.is_active:
            return JsonResponse({"error": "Token is deactivated"}, status=403)

        if token.expires_at < timezone.now():
            token.is_active = False
            token.save()
            return JsonResponse({"error": "Token has expired"}, status=403)

        request.user = token.user
        request.auth_token = token

        return view_func(request, *args, **kwargs)
    return _wrapped_view