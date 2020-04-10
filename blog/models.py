from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

import random

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True) # Blank - если тру, значит поле может быть пустым.
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True) # Присохранении в базе данных, это поле будет заполнено.

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']

# class Message(models.Model):
#     body = models.TextField(blank=True, db_index=True) # Blank - если тру, значит поле может быть пустым.
#     date_pub = models.DateTimeField(auto_now_add=True) # Присохранении в базе данных, это поле будет заполнено.
#     message_id = models.CharField(max_length=150, db_index=True)
#
#     def __str__(self):
#         return self.body

class MessageChat(models.Model):
    body = models.TextField(blank=True, db_index=True) # Blank - если тру, значит поле может быть пустым.
    date_pub = models.DateTimeField(auto_now_add=True) # Присохранении в базе данных, это поле будет заполнено.
    message_id = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.body


# class User(models.Model):
#     name = models.CharField(max_length=50, db_index=True)
#     last_name = models.CharField(max_length=50, db_index=True)
#     first_name = models.CharField(max_length=50, db_index=True)
#     id = random.randint(10000000, 99999999)
