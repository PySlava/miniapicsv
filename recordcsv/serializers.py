from rest_framework import serializers
from .models import Upload, Person


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

