import os
from PIL import Image, ExifTags
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True,verbose_name='(250x250)')
    name = models.CharField(max_length=20, db_index=True)
    slug = models.SlugField(max_length=20, db_index=True, unique=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_show', args=[self.slug])



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete = models.CASCADE)
    product_no = models.CharField(max_length=25,default='Ürün Kodu Giriniz')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    list_image = models.ImageField(upload_to='products/%y/%m/%d', blank=True,verbose_name='370x410')
    technic = models.ImageField(upload_to='products/%y/%m/%d', blank=True, verbose_name='Teknik Çizim')
    info = models.TextField(default='Ürün Aaçıklama')
    description = RichTextUploadingField(blank=True)
    shop = RichTextUploadingField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField()
    list = models.BooleanField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    seo = models.CharField(max_length=500,default="Seo için Bilgi Giriniz.")
    key = models.CharField(max_length=550,default="Keyword için Giriş")
    news = models.BooleanField(default=False)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/',verbose_name='700x778')

    def __str__(self):
        return self.title


class Rules(models.Model):
   no = models.CharField(max_length=200, db_index=True)
   sss = RichTextUploadingField(blank=True)


   def __str__(self):
       return self.no






class Discount(models.Model):
    name = models.CharField(max_length=50,blank=True,verbose_name='Name')
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True, verbose_name='467x459')
    title = models.CharField(max_length=50,blank=True,verbose_name='Başlık')
    info = models.CharField(max_length=50,blank=True,verbose_name='İnfo')
    link = models.CharField(max_length=50,blank=True,verbose_name='Yönledirme')
    vercital = models.ImageField(upload_to='products/%y/%m/%d', blank=True, verbose_name='184x322')



    def __str__(self):
        return self.name



