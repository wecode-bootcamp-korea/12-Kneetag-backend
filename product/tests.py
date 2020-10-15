import json
from django.test import TestCase, Client
from .models     import Category, Series, Product, SubImage, Size, Type

class ProductListViewTest(TestCase):
    maxDiff = None
    def setUp(self):   
        category = Category.objects.create(
            id =1,
            name = "categoryFirst"
            )
        
        series   = Series.objects.create(
            id =1,
            name = "seriesFirst", 
            category_id = category.id,
            price = 80000,
            sub_detail = "bestSeries"
            )
        
        Product.objects.create(
            id =1,
            name = "test1product", 
            image_url = "http://kneetag.jpg", 
            series_id = series.id,   
        )
        Product.objects.create(
            id =2,
            name = "test2product", 
            image_url = "http://kneetag.jpg", 
            series_id = series.id,   
        )
        
    def tearDown(self):
        Product.objects.all().delete()
         
    def test_productlistview_get_succeess(self):
        client = Client()
        
        response = self.client.get('/product') 
        product_list =[
                {
                "categoryName" : product.series.category.name,
                "seriesName"   : product.series.name,
                "seriesPrice"  : 80000,
                "id"           : product.id,
                "mainImage"    : "http://kneetag.jpg",
                } for product in Product.objects.all()
            ]
        self.assertEqual(response.json(), {"message":product_list})
        self.assertEqual(response.status_code, 200)
           
class ProductViewTest(TestCase):
    def setUp(self):   
        category = Category.objects.create(
            id =1,
            name = "categoryFirst"
            )
        
        series   = Series.objects.create(
            id =1,
            name = "seriesFirst", 
            category_id = category.id,
            price = 80000,
            sub_detail = "bestSeries"
            )
        
        sizes = Size.objects.create(
            id = 1,
            name = "sizename",
            series_id = 1
        )
        
        Product.objects.create(
            id =1,
            name = "test1product", 
            image_url = "http://kneetag.jpg", 
            series_id = series.id,   
        )
        
        Type.objects.create(
            id = 1,
            name = "typeid"
        )
        
        SubImage.objects.create(
            id = 1,
            image_url = "kneetagsub",
            product_id = 1,
            type_id = 1
        )
        
    def tearDown(self):
        Product.objects.all().delete()
        
    def test_productview_get_succeess(self):
        client = Client()
        response = self.client.get('/product/1')  
        data = {
                "size"        : ["sizename"],
                "description" : "bestSeries",
                "detailImage" : ["kneetagsub"],
                "name"        : "test1product",
                "price"       : 80000,
                "title"       : "seriesFirst", 
            }   
        self.assertEqual(response.json(), {"message" : data})
        self.assertEqual(response.status_code, 200)
    
    def test_productlistview_get_keyerror(self):
        client = Client()
        
        response = self.client.get('/product/13') 
        data = {
                "sidze"       : ["sizename"],
                "description" : "bestSeries",
                "detailImage" : ["kneetagsub"],
                "name"        : "test1product",
                "price"       : 80000,
                "title"       : "seriesFirst", 
            }  
        
        self.assertEqual(response.json(), {"message" : 'NOT_EXIST'})
        self.assertEqual(response.status_code, 400)        