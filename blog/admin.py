from django.contrib import admin
from .models import Post, Comment, registerCamera, Country, City
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(registerCamera)
admin.site.register(Country)
admin.site.register(City)
