import decimal
import json

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    slug = models.SlugField(max_length=255,unique=True,db_index=True,verbose_name='slug')
    desc = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True, verbose_name='Фото')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория',null=True)

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = "Пиццы"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug':self.slug})

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name = 'Категория')
    slug = models.SlugField(max_length=255,unique=True,db_index=True,verbose_name='slug',primary_key=True)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = "Категории"
        ordering = ['slug','name']
    def __str__(self):
        return self.name


