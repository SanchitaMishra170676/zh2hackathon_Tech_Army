from django.contrib import admin

# Register your models here.

from .models import UserDetail, SavedAccount
admin.site.register(UserDetail)
admin.site.register(SavedAccount)