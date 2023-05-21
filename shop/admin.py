from django.contrib import admin
from django import forms
from .models import Category,Product ,Rules ,Images , Discount
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from yoga.models import Slider


class Gallery(admin.TabularInline):
    model = Images

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']
    prepopulated_fields = {'slug':('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','category','price','available','created']
    list_filter = ['available','created']
    list_editable = ['price','available']
    prepopulated_fields = {'slug':('name',)}
    inlines = (Gallery,)

class ModelClass:
    ## content = models.TextField()bu ile modeldeki classı belirleriz burayada dikkat.
    description = RichTextUploadingField()

class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

class SliderAdmin(admin.ModelAdmin):
    list_display = ['title']


class RulesAdmin(admin.ModelAdmin):
    list_display = ['no']



class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Discount,DiscountAdmin)
admin.site.register(Rules,RulesAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.site_header = 'Batı Grup / Developer @ İhsan Gürol Demirtaş'



