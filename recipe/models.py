from PIL import Image
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('NS', 'Не указано'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    fav = models.CharField(max_length=300, blank=True)
    cart = models.CharField(max_length=1000, blank=True)
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default='NS')
    birth_date = models.DateField(default='1990-01-01')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class CommentsManager(models.Manager):
    def create_comment(self, recipe_id, user, comment_text, likes):
        comment = self.create(recipe_id=recipe_id, user=user, comment_text=comment_text, likes=likes)
        # do something with the book
        return comment

class Comments(models.Model):
    recipe_id = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, unique=False)
    comment_text = models.TextField(max_length=150)
    likes = models.IntegerField(default=0)
    objects = CommentsManager()


class Reply(models.Model):
    comments = models.OneToOneField(Comments, on_delete=models.CASCADE)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, unique=False)
    reply_text = models.TextField(max_length=150)
    likes = models.IntegerField(default=0)
