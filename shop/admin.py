from django.contrib import admin

from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug',)
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available',)
	list_filter = ('available', 'created',)
	list_editable = ('price',)
	prepopulated_fields = {'slug': ('name',)}
	raw_id_fields = ('categories',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	pass