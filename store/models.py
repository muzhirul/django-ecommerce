import imp
from statistics import mode
from unicodedata import category
from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products', blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    
    def __str__(self):
        return self.product_name