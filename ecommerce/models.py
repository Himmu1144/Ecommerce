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