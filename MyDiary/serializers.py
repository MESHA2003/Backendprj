from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']


class DiaryEntrySerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)  # Include tag name for display

    class Meta:
        model = DiaryEntry
        fields = ['id', 'title', 'content', 'created_at', 'entry_date', 'tag', 'tag_name']
        read_only_fields = ['created_at']        
