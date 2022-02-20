from django.contrib import admin
from recipe.models import Profile, Comments, Reply

# Register your models here.

admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Reply)