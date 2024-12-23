from django.contrib import admin
from .models import *

# Create your views here.
admin.site.register(DiaryEntry)
admin.site.register(UserSetting)
admin.site.register(Tag)
admin.site.register(DiaryEntryTag)
