from rest_framework import serializers
from . import models

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = ('id', 'name', 'user', 'max_block_order', 'created_at', 'modified_at', )
        read_only_fields = ('user', )

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Block
        fields = ('id', 'document', 'type', 'order', 'next_block_pk', 'content', 'equation', 'image', 'created_at', 'modified_at', )
        read_only_fields = ('document', 'user', )
