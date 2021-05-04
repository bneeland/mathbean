from rest_framework import serializers
from . import models

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = ("id", "name", "user", "created_at", "modified_at", )
        read_only_fields = ('user', )