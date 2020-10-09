from django.test                    import TestCase, Client
from my_settings                    import SECRET, ALGORITHM, EMAIL
from .models                        import User
from .text                          import message
from .utils                         import login_decorator
from unittest.mock                  import patch, MagicMock
import json
import jwt
import bcrypt
import datetime
import requests

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            name      = 'jane',
            email     = 'test1@nate.com',
            password  = None,
            is_active = False
        )
        User.objects.create(
            name      = 'tom',
            email     = 'test2@nate.com',
            password  = None,
            is_active = False
        )
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
        self.token = jwt.encode({'user_id':User.objects.get(name='jane').id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_email_send_post_success(self):
        client = Client()
        user = {
            'name'  : 'dasom',
            'email' : '01095542042@naver.com'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

    def test_signup_already_exist_name(self):
        client = Client()
        user = {
            'name'  : 'jane',
            'email' : 'test3@nate.com'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'ALREADY EXIST'
            }
        )

    def test_signup_already_exist_email(self):
        client = Client()
        user = {
            'name'  : 'james',
            'email' : 'test2@nate.com'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'ALREADY EXIST'
            }
        )

    def test_signup_keyerror(self):
        client = Client()
        user = {
            'nam'   : 'erin',
            'email' : 'test4@nate.com'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message':'KEY ERROR'
            }
        )

    def test_email_validate_error(self):
        client = Client()
        user = {
            'name'  : 'judy',
            'email' : 'test5nate.com'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'INVALID EMAIL'
            }
        )

    def test_update_password_success(self):
        client = Client()
        
        headers = {'HTTP_Authorization':self.token}
        
        user = {
            'password' : '12345'
        }
        response = client.patch('/user/signup', json.dumps(user), **headers, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'
            }
        )

class ActivateTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            name      = 'jane',
            email     = 'test1@nate.com',
            password  = None,
            is_active = False
        )
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':user.id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')
    
    def tearDown(self):
        User.objects.all().delete()

    def test_get_token_success(self):
        client  = Client()
        headers = {'HTTP_Authorization':self.token}

        response = client.get('/user/activate', **headers, content_type='application/json')
        self.assertEqual(response.json(), 
            {
                'Authorization':self.token
            }
        )