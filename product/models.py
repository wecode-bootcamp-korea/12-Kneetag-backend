from django.db   import models
from user.models import User

class Product(models.Model):
    name       = models.CharField(max_length = 100) 
    image_url  = models.URLField()
    series     = models.ForeignKey('Series', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)   
        
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "products"   

class Category(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
                                    
class Series(models.Model):
    name        = models.CharField(max_length = 100)
    category    = models.ForeignKey('Category', on_delete = models.CASCADE)
    price       = models.DecimalField(max_digits = 10, decimal_places = 2)
    sub_detail  = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "series"
             
class Size(models.Model):
    name   = models.CharField(max_length = 80)   
    series = models.ForeignKey('Series', on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "sizes"
               
class SubImage(models.Model):
    image_url = models.CharField(max_length = 300)
    product   = models.ForeignKey('Product', on_delete = models.CASCADE)
    type      = models.ForeignKey('Type', on_delete = models.CASCADE)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        db_table = "sub_images"
        
class Type(models.Model):
    name = models.CharField(max_length = 100) 
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "types"   
        
class Detail(models.Model):
    title   = models.CharField(max_length = 200)
    series  = models.ForeignKey('Series', on_delete = models.CASCADE)
    content = models.CharField(max_length = 600)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "details"           
