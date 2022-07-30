from turtle import heading
from django.db import models

# Create your models here.

class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500,default='')
    content = models.CharField(max_length=5000,default='')
    image = models.ImageField(upload_to='blog/images')
    date = models.DateField()

    def __str__(self):
        return self.title

