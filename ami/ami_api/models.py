from django.db import models

# Create your models here.

class GeoNote(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=12,decimal_places=4,default=0,)
    longitude = models.DecimalField(max_digits=12,decimal_places=4, default=0)
    value =  models.CharField(max_length=60)
    def __str__(self):
        return self.value

class StackedImage(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now=True)
    filepath = models.URLField(max_length=200)

class OverlayImage(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    index_name = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now=True)
    filepath = models.URLField(max_length=200)
