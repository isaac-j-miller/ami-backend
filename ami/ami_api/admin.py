from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(GeoNote)
admin.site.register(StackedImage)
admin.site.register(OverlayImage)
admin.site.register(User)
