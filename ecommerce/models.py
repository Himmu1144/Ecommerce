from email.policy import default
from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    prod_name = models.CharField(max_length=55)
    prod_desc = models.CharField(max_length=2000)
    price = models.IntegerField(default=0)
    images = models.ImageField(upload_to='ecommerce/images', default='')
    category = models.CharField(max_length=50, default='')
    subcategory = models.CharField(max_length=50, default='')
    pub_date = models.DateField()

    def __str__(self):
        return self.prod_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=55)
    email = models.CharField(max_length=50)
    desc = models.CharField(max_length=2000)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=55)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=2000)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    Json_Items = models.CharField(max_length=5000, default='')

class Order_Update(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=100)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self): 
        return str(self.order_id) + ' ' + self.update_desc[:35]