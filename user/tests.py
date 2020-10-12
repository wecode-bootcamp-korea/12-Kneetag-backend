from unittest.mock                  import patch, MagicMock
import json
import jwt
import bcrypt
import datetime
import requests

from django.test                    import TestCase, Client
from my_settings                    import SECRET, ALGORITHM, EMAIL

from .models                        import User
from .text                          import message
from .utils                         import login_decorator

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

class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            name      = 'tom',
            email     = 'test11@naver.com',
            password  = bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active = True
        )
    
    def tearDown(self):
        User.objects.all().delete()

    def test_signin_name_post_success(self):
        client = Client()

        user = {
            'user'     : 'tom',
            'password' : '12345',
            'is_active': True
        }
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':User.objects.get(name=user['user']).id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')
        
        equal = [i for i in response.json().keys()]
        self.assertEqual(equal[0], 'Authorization')
        self.assertEqual(response.status_code, 200)

    def test_signin_email_post_success(self):
        client = Client()

        user = {
            'user'     : 'test11@naver.com',
            'password' : '12345',
            'is_active': True
        }

        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':User.objects.get(email=user['user']).id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')
        
        response = client.post('/user/signin', json.dumps(user), content_type='application/json')
        
        equal = [i for i in response.json().keys()]
        self.assertEqual(equal[0], 'Authorization')
        self.assertEqual(response.status_code, 200)

    def test_signin_key_error(self):
        client = Client()

        user = {
            'user'     : 'test11@naver.com',
            'pasword'  : '12345',
            'is_active': True
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY ERROR'
            }
        )

    def test_signin_user_email_not_exist(self):
        client = Client()

        user = {
            'user'     : 'test1@naver.com',
            'password' : '12345',
            'is_active': True
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'INVALID REQUEST'
            }
        )

    def test_signin_user_name_not_exist(self):
        client = Client()

        user = {
            'user'     : 'jame',
            'password' : '12345',
            'is_active': True
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'INVALID REQUEST'
            }
        )

    def test_signin_wrong_password(self):
        client = Client()

        user = {
            'user'     : 'test11@naver.com',
            'password' : '123433',
            'is_active': True
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'WRONG PASSWORD'
            }
        )

class GoogleSignInTest(TestCase):
    
    def setUp(self):
        user = User.objects.create(
            name      = 'tom',
            email     = 'test11@gmail.com',
            password  = bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active = True
        )
        
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':user.id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch('user.views.requests')
    def test_user_google_signin_user_exist(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'email':'test11@gmail.com',
                    'name' :'tom'
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        headers  = {'HTTP_Authorization':self.token}
        response = client.post('/user/googlesignin', **headers, content_type='application/json')
        
        user       = User.objects.get(name='tom')
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':user.id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

        equal = [i for i in response.json().keys()]
        self.assertEqual(equal[0], 'Authorization')
        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_user_google_signin_user_not_exist(self, mocked_requests):
        client = Client()
        
        headers = {'HTTP_Authorization':self.token}
        
        class MockedResponse:
            def json(self):
                return {
                    'email':'test@gmail.com',
                    'name' :'tomi'
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        response = client.post('/user/googlesignin', **headers, content_type='application/json')

        new_user   = User.objects.create(name='tomi', email='test@naver.com', is_active=True)
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':new_user.id,'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

        equal = [i for i in response.json().keys()]
        self.assertEqual(equal[0], 'Authorization')
        self.assertEqual(response.status_code, 200)