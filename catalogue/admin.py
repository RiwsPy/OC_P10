from django.contrib import admin
from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['code', 'product_name']
    readonly_fields = ['code']
