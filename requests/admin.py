from django.contrib import admin
from .models import Request, Category, AbsUser

admin.site.register(Request)
admin.site.register(Category)
admin.site.register(AbsUser)