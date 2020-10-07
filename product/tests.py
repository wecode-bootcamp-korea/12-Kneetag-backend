import json
from django.test import TestCase, Client
from .models     import Category, Series, Product

class ProductListViewTest(TestCase):
    def setUp(self):
        Product.objects.create() 
        
    def tearDown(self):
        Product.objects.all().delete()
        
    def test_productlistview_get_succeess(self):
        client = Client()
        response = self.client.get('/product/1')
        self.assertEqual(response.json(), {
            "data" : [
                {
                    "category_name" : 1,
                    "title"         : "프로덕트시리즈",
                    "price"         : "86000",
                    "image"         : "프로덕트대표이미지",
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

class ProductViewTest(TestCase):
    def setUp(self):
        Product.objects.create()
        
    def tearDown(self):
        Product.objects.all().delete()
        
    def test_productview_get_succeess(self):
        client = Client()
        response = self.client.get(f'/product/{Product.objects.first().id')
        self.assertEqual(response.json(), {
            "data": {
                "product": {
                    "id"          : 1,
                    "title"       : "프로덕트시리즈",
                    "price"       : "86000",
                    "description" : "테스트 상품타입",
                    "name"        : "프로덕트이름",
                    "size"        : "상품사이즈",
                    "detailImage" : "상품세부이미지",
                    }
                }
            }
        })
        self.assertEqual(response.status_code, 200)