from django.contrib import admin

from recipe.models import Profile, Comments, Reply


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birth_date', 'fav')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe_id', 'user', 'comment_text', 'likes')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass
