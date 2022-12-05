from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class Products(models.Model):
    product = models.CharField(max_length=255)
    category = models.ManyToManyField(Category, related_name="catergory")
    price = models.IntegerField()

    def __str__(self):
        return self.product

