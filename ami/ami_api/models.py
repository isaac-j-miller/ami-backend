from django.db import models
from .customutils import *

# Create your models here.

class GeoNote(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now=False)
    latitude = models.DecimalField(max_digits=14,decimal_places=10,default=0)
    longitude = models.DecimalField(max_digits=14,decimal_places=10, default=0)
    value =  models.CharField(max_length=60)
    def __str__(self):
        return self.value

class User(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=20)
    fields = models.CharField(max_length=10000)
    def __str__(self):
        return self.user

class StackedImage(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    date = models.DateField(auto_now=False)
    filepath = models.CharField(max_length=200)
    demfilepath = models.CharField(max_length=200)

class OverlayImage(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    index_name = models.CharField(max_length=60)
    date = models.DateField(auto_now=False)
    filepath = models.CharField(max_length=200)
    tiffilepath = models.CharField(max_length=200)
    scalefilepath = models.CharField(max_length=200)

class RawImageSet(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.CharField(max_length=60)
    field = models.CharField(max_length=60)
    date = models.DateField(auto_now=False)
    filepath = models.CharField(max_length=200)

class Index(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    long_name = models.CharField(max_length=60, default=' ')
    summary = models.CharField(max_length=500, default=' ')
    def __str__(self):
        return self.name

class Field(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=60, default='')
    user = models.CharField(max_length=60)
    latitude = models.DecimalField(max_digits=14,decimal_places=10,default=0)
    longitude = models.DecimalField(max_digits=14,decimal_places=10, default=0)
    def __str__(self):
        return self.name