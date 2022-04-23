import imp
from pyexpat import model
from django.contrib import admin
from .models import Product, ReviewRating, Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variant_category','variation_value','create_date','is_active')
    list_editable = ('variation_value', 'is_active',)
    list_filter = ('product','variant_category','variation_value',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)