from django.views                   import View
from django.http                    import JsonResponse
from django.db.models               import Q
from django.core.exceptions         import ValidationError
from django.core.validators         import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail               import EmailMessage
from my_settings                    import SECRET, ALGORITHM, EMAIL
from .models                        import User
from .text                          import message
from .utils                         import login_decorator
import json
import jwt
import bcrypt
import datetime
import requests

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])

            if User.objects.filter(Q(email=data['email']) | Q(name=data['name'])).exists():
                return JsonResponse({'message':'ALREADY EXIST'}, status=400)
            
            user = User.objects.create(
                email     = data['email'],
                name      = data['name'],
                password  = None,
                is_active = False
            )

            name         = user.name
            domain       = get_current_site(request).domain
            expire       = datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
            token        = jwt.encode({'user_id':user.id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')
            message_data = message(domain, token, name)

            mail_title = '안녕하세요. freitag입니다. 이메일 인증을 완료해주세요.'
            to_mail    = data['email']
            email      = EmailMessage(mail_title, message_data, to=[to_mail])
            email.send()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except ValidationError:
            return JsonResponse({'message':'INVALID EMAIL'}, status=400)

    @login_decorator
    def patch(self, request):
        data            = json.loads(request.body)
        user            = User.objects.get(id=request.user.id)
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password   = hashed_password 
        user.save()
        
        return JsonResponse({'message':'SUCCESS'}, status=200)

class ActivateView(View):
    @login_decorator
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user.is_active = True
        user.save()
        expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        access_token = jwt.encode({'user_id':user.id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

        return JsonResponse({'Authorization':access_token}, status=200)