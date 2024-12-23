from typing import Any
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
        
class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    entry_date = models.DateField()

    def __str__(self):
        return self.title

class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    language_preference = models.CharField(max_length=20, default='English')
    
    def __str__(self):
        return f"Setting for {self.user.username}"
    


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class DiaryEntryTag(models.Model):
    diary_entry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.diary_entry.title} - {self.tag.name}"

