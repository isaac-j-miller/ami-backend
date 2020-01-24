from rest_framework import serializers

from .models import *

class GeoNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeoNote
        fields = ('id','user','field','date','latitude','longitude','value')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','user','password','fields')

class StackedImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StackedImage
        fields = ('id','user','field','date','filepath','demfilepath')

class OverlayImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OverlayImage
        fields = ('id','user','field','date','index_name','filepath', 'tiffilepath', 'scalefilepath')

class RawImageSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RawImageSet
        fields = ('id','user','field','date','filepath')

class IndexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Index
        fields = ('name','summary')

class FieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Field
        fields = ('id','name','user','latitude', 'longitude')
