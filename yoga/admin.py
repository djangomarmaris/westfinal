from django.contrib import admin

# Register your models here.
from yoga.models import Blog , About , kvvk


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug': ('title',)}



class AboutAdmin(admin.ModelAdmin):
    list_display = ['title']



class kvvkAdmin(admin.ModelAdmin):
    list_display = ['name']



admin.site.register(kvvk,kvvkAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(About,AboutAdmin)