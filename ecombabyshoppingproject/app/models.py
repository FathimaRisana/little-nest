from django.db import models

import os
import datetime
from django.utils.text import slugify

# Create your models here.

def get_file_path(request, filename):
    orginal_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%n%d%H:%%M:%S')
    filename = "%s%s" % (nowTime, orginal_filename)
    return os.path.join('uploads/', filename)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name




class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    price = models.FloatField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    #
    # def __str__(self):
    #     return f"{self.user.username} - {self.product.name} ({self.quantity})"


    def get_total_price(self):
        return self.product.price * self.quantity


