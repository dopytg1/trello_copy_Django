from django.db import models
from django.utils.text import slugify

from trello_main.models import CustomUser


class Board(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    background = models.ImageField(upload_to='static/background', blank=True)

    user_id = models.ManyToManyField(CustomUser, blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Card(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return self.title


class Column(models.Model):
    title = models.CharField(max_length=30)
    cards_inside = models.ManyToManyField(Card)

    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CheckList(models.Model):
    title = models.CharField(max_length=50)
    is_checked = models.BooleanField(default=False)

    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# class CheckListElement(models.Model):
#     title = models.CharField()

class Mark(models.Model):
    hex_color = models.CharField(max_length=10)

    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.author + self.column_id.title

