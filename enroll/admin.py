from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(PredictedVideo)

# admin.py
from django.contrib import admin
from .models import CheatingDetection

admin.site.register(CheatingDetection)



