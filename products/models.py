from django.db import models
import uuid


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)
    # product = models.ManyToManyField(Products, max_length=255)

    def __str__(self):
        return self.category

class Products(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4())
    product = models.CharField(max_length=255)
    category = models.ManyToManyField(Category, related_name="catergory")
    price = models.IntegerField()

    def __str__(self):
        return self.product

