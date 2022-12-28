from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Account)
admin.site.register(Questions)
admin.site.register(Answer)

admin.site.site_header = 'Awards'
