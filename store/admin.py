import imp
from pyexpat import model
from django.contrib import admin
from .models import Product, ProductGallery, ReviewRating, Variation
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variant_category','variation_value','create_date','is_active')
    list_editable = ('variation_value', 'is_active',)
    list_filter = ('product','variant_category','variation_value',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)