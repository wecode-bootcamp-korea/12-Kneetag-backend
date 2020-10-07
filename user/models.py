from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField(max_length=100)
    password   = models.CharField(max_length=100, null=True)
    is_active  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'users'

class Address(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name        = models.CharField(max_length=100)
    last_name         = models.CharField(max_length=100)
    company           = models.CharField(max_length=100, null=True)
    address_first     = models.CharField(max_length=100)
    address_second    = models.CharField(max_length=100, null=True)
    district          = models.CharField(max_length=100)
    province          = models.CharField(max_length=100)
    post_code         = models.IntegerField()
    phone_number      = models.CharField(max_length=100)

    class Meta:
        db_table = 'addresses'