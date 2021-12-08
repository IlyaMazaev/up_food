from django.db import models


# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    products = models.CharField(max_length=100)
    how_to_cook = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    portions = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    types = models.CharField(max_length=100)
    # some additional fields, currently not used
    date_time_added = models.CharField(max_length=100)
    creator_info = models.CharField(max_length=100)
    some_additional_info = models.CharField(max_length=100)
