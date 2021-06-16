from django.db import models
from rest_framework import serializers
from .models import TheClass

class TheClassModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= TheClass
        fields= "__all__"
        depth = 1