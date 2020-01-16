from rest_framework import serializers

from .models import *

class GeoNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeoNote
        fields = ('id','user','field','date','latitude','longitude','value')

class StackedImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StackedImage
        fields = ('id','user','field','date','filepath')

class OverlayImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OverlayImage
        fields = ('id','user','field','date','index_name','filepath')