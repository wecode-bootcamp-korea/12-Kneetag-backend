from django.http import JsonResponse
from .models     import User
from my_settings import SECRET, ALGORITHM
import jwt
import json

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if not 'Authorization' in request.headers:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        try:
            access_token = request.headers['Authorization']
            data         = jwt.decode(access_token, SECRET['secret'], algorithm = ALGORITHM)
            user         = User.objects.get(id=data['user_id'])
            request.user = user

        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID TOKEN'}, status=400)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'TOKEN EXPIRED'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper