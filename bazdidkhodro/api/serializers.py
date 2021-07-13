from rest_framework import serializers
from rest_framework.utils.representation import serializer_repr

from bazdidkhodro.models import (Image,Insurer,Visit,Document,DocumentFile)
from account.models import User


class InsurerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = ('name','mobile','address','p1','p2','p3','p4','created_by',"pelak")


class ImageCreateSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = ['visit','img']


class DocumentFileCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = DocumentFile
        fields = ['document','file']


class VisitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('id','insurer', 'visitor', 'year')
        read_only_fields = ['id']


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id','insurer','employee')
        read_only_fields = ['id']


class VisitShowSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    insurer_name = serializers.ReadOnlyField()

    class Meta:
        model = Visit
        fields = ('insurer', 'visitor', 'year','images','insurer_name')


class InsurerShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = ('id', 'name', 'mobile', 'address', 'pelak')


