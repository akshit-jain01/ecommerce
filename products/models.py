from django.db import models
import uuid

from django.utils.text import slugify

class ColorVariant(models.Model):
    color = models.CharField()
    color_code = models.CharField()
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
    
    def __str__(self):
        return self.category_name

class Products(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4())
    product_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    # image = models.ImageField()

    def __str__(self):
        return self.product_name


