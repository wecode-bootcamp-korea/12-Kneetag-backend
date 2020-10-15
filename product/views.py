import json
from django.views import View
from django.http  import JsonResponse
from .models      import Category, Series, Product, SubImage

class ProductListView(View):
    def get(self,request):
            product_list =[
                {
                "categoryName" : product.series.category.name,
                "seriesName"   : product.series.name,
                "seriesPrice"  : int(product.series.price),
                "id"           : product.id,
                "mainImage"    : product.image_url,
                } for product in Product.objects.all()
            ]
            return JsonResponse({"message" : product_list}, status = 200)     

class ProductView(View):
    def get(self, request, product_id):
        try:        
            selected_product = Product.objects.select_related('series').prefetch_related('subimage_set','series__size_set').get(pk = product_id)  
                
            data = {
                "size"        : [sizes.name for sizes in selected_product.series.size_set.all()],
                "description" : selected_product.series.sub_detail,
                "detailImage" : [image.image_url for image in selected_product.subimage_set.all()],
                "name"        : selected_product.name,
                "price"       : int(selected_product.series.price),
                "title"       : selected_product.series.name, 
            }   
            return JsonResponse({"message":[data]}, status = 200) 

        except Product.DoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST"}, status = 400)