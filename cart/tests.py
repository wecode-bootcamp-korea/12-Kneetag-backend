import jwt
import bcrypt
import json
import datetime

from django.test import TestCase, Client
from my_settings import SECRET, ALGORITHM

from user.utils     import login_decorator
from .models        import Cart 
from user.models    import User
from product.models import Product, Category, Series, Size

class CartTest(TestCase):
    def setUp(self):
        User.objects.create(
            id        = 1,
            name      = 'test1',
            email     = 'test1@gmail.com',
            password  = bcrypt.hashpw('123123123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_active = True
        )
        Category.objects.create(
            id   = 1,
            name = 'test'
        )
        Series.objects.create(
            id          = 1,
            name        = 'test',
            category_id = 1,
            price       = 10000,
            sub_detail  = 'test'
        )
        Product.objects.create(
            id        = 1,
            name      = 'test1',
            image_url = 'test.test',
            series_id = 1
        )
        Product.objects.create(
            id        = 2,
            name      = 'test1',
            image_url = 'test.test',
            series_id = 1
        )
        Product.objects.create(
            id        = 3,
            name      = 'test1',
            image_url = 'test.test',
            series_id = 1
        )
        Size.objects.create(
            id=1,
            name='s',
            series_id=1
        )
        Size.objects.create(
            id=2,
            name='m',
            series_id=1
        )
        Cart.objects.create(
            id         = 1,
            count      = 1,
            product_id = 1,
            user_id    = 1,
            size_id    = 1
        )
        Cart.objects.create(
            id         = 2,
            count      = 1,
            product_id = 3,
            user_id    = 1,
            size_id    = 2
        )
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
        self.token = jwt.encode({'user_id':1, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Cart.objects.all().delete()

    def test_post_cart_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        cart = {
            'count'      : 1,
            'product_id' : 2,
            'size_id'    : 1
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_post_cart_same_user_product_already_exist(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        cart = {
            'count'      : 1,
            'product_id' : 1,
            'size'       : 1
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_post_cart_key_error(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        cart = {
            'cont'       : 1,
            'product_id' : 2,
            'size'       : 2
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'KEY ERROR'})
        self.assertEqual(response.status_code, 400)

    def test_get_cart_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        response = client.get('/cart?offset=1&limit=4', **headers)
        self.assertEqual(response.json(), 
            {
                'cart_list':[
                    {
                        'id'         : 1,
                        'product_id' : 1,
                        'name'       : 'test1',
                        'image'      : 'test.test',
                        'price'      : 10000,
                        'count'      : 1,
                        'size'       : 's',
                    },
                    {
                        'id'         : 2,
                        'product_id' : 3,
                        'name'       : 'test1',
                        'image'      : 'test.test',
                        'price'      : 10000,
                        'count'      : 1,
                        'size'       : 'm',
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_update_cart_count_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        data = {
            'cart_button' : '+'
        }
        response = client.patch('/cart/1', json.dumps(data), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_update_cart_count_is_one_request_minus(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        data = {
            'cart_button' : '-'
        }
        response = client.patch('/cart/2', json.dumps(data), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_update_cart_key_error(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        data = {
            'button' : '+'
        }
        response = client.patch('/cart/2', json.dumps(data), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'KEY ERROR'})
        self.assertEqual(response.status_code, 400)

    def test_update_cart_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        data = {
            'cart_button' : '-'
        }
        response = client.patch('/cart/5', json.dumps(data), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)

    def test_delete_cart_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        response = client.delete('/cart/1', **headers)
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_delete_cart_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        response = client.delete('/cart/10',  **headers)
        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)