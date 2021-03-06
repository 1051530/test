from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated', 'sell']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available', 'sell']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)

