from django.contrib import admin
from .models import Order, OrderItem ,Reservation





class Back_Admin(admin.ModelAdmin):
    list_display = ["author", "order_no", "cargo","created_date","case"]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# 'paid', 'tokenCheck',

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'city', 'created']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]



class SenderAdmin(admin.ModelAdmin):
    list_display = ['author']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name']



admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Order, OrderAdmin)

