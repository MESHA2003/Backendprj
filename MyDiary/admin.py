from django.contrib import admin
from .models import *

# Create your views here.
admin.site.register(DiaryEntry)
admin.site.register(Tag)

