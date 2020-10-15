import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from user.utils       import login_decorator
from .models          import Cart
from user.models      import User
from product.models   import Product


class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            if Cart.objects.filter(Q(product_id=data['product_id']) & Q(user_id=request.user.id)).exists():
                return JsonResponse({'message':'INVALID REQUEST'}, status=400)
            
            Cart.objects.create(
                count      = data['count'],
                product_id = data['product_id'],
                user_id    = request.user.id,
                size_id    = data['size_id']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
    
    @login_decorator
    def get(self, request):
        cart_list    = Cart.objects.filter(user_id=request.user.id).select_related('product__series')

        results = [{
            'id'         : data.id,
            'product_id' : data.product.id,
            'name'       : data.product.name,
            'image'      : data.product.image_url,
            'price'      : int(data.product.series.price),
            'count'      : data.count,
            'size'       : data.size.name
        } for data in cart_list]

        return JsonResponse({'cart_list':results}, status=200)

    @login_decorator
    def patch(self, request, cart_id):
        try:
            data = json.loads(request.body)
            cart = Cart.objects.get(id=cart_id)

            if data['cart_button'] == '+':
                cart.count += 1
                cart.save()
            elif data['cart_button'] == '-':
                if cart.count == 1:
                    return JsonResponse({'message':'INVALID REQUEST'}, status=450)
                cart.count -= 1
                cart.save()
            
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=455)
        except Cart.DoesNotExist:
            return JsonResponse({'message':'NOT FOUND'}, status=404)

    @login_decorator
    def delete(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            cart.delete()
            
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message':'NOT FOUND'}, status=404)