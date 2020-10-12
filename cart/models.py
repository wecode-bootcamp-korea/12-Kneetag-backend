from django.db       import models
from user.models     import User
from product.models  import Product, Size

class Cart(models.Model):
    count      = models.IntegerField(default=1)
    product    = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    size       = models.ForeignKey('product.Size', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'carts'