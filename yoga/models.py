from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.shortcuts import render, redirect ,get_object_or_404 ,reverse
# Create your models here.



class Slider(models.Model):
    title = models.CharField(max_length=300, default='Title')
    low = models.CharField(max_length=300, default='Low Title')
    info = models.CharField(max_length=300, default='Marka İsimi')
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True,verbose_name='Resim : (1015x765)')
    link = models.CharField(max_length=3000, default='Yönlendirilicek URL')


    def __str__(self):
        return self.title





class Blog(models.Model):
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True, verbose_name='Resim : (550x350)')
    list = models.ImageField(upload_to='products/%y/%m/%d', blank=True, verbose_name='Resim : (850x530)')
    title = models.CharField(max_length=1000, default='Title')
    mini_info = RichTextUploadingField()
    info = RichTextUploadingField()
    slug = models.SlugField(max_length=200, db_index=True)



    def __str__(self):
        return self.title


    def get_absolute_url(self):

        return reverse('yoga:blog_detail',args=[self.slug])



class About(models.Model):
    title = models.CharField(max_length=1000, default='Title')
    info = RichTextUploadingField()
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True, verbose_name='Resim : (370x610)')



    def __str__(self):
        return self.title



class kvvk(models.Model):
    name = models.CharField(max_length=200, db_index=True,default='Açıklama Başlığı',verbose_name='Name')
    kvvk = models.FileField(upload_to='products/katalog/%y/%m/%d')

    def __str__(self):
        return self.name