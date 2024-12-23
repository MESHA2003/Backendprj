from rest_framework import serializers
from .models import *


class DiaryEntryserializer(serializers.ModelSerializer):

    class Meta:
        
        model=DiaryEntry
        fields='__all__'

class Usersettingserializer(serializers.ModelSerializer):
    class Meta:
        model= UserSetting
        fields='__all__'

class Tagserializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        field='__all__'

class DiaryEntryTagserializer(serializers.ModelSerializer):

    class Meta:
        model = DiaryEntryTag
        field='__all__'