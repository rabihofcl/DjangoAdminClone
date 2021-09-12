from django.db import models

# Create your models here.
 
class Product_Category(models.Model):
    category_image = models.CharField(max_length=1500)
    category_name = models.CharField(max_length=50)
    

class Product(models.Model):
    image = models.CharField(max_length=1500)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.IntegerField()





