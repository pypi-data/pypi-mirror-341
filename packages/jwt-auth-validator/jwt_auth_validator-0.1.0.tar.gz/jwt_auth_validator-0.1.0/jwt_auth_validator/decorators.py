from functools import wraps
from django.http import JsonResponse
from .jwt_utils import decode_token
from .settings import settings

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return JsonResponse({"error": "Authorization header is missing"}, status=401)

            try:
                # JWT decode - verify 
                token = token.split(" ")[1]  # Bearer token
                payload = decode_token(token, settings.JWKS_URL)
                
                # check permissions
                user_permissions = payload.get("permissions", [])
                if permission not in user_permissions:
                    return JsonResponse({"error": "Forbidden"}, status=403)

                # run main function
                return func(request, *args, **kwargs)
            
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=401)
        
        return wrapper
    return decorator