from django.contrib import admin
from .models import FitFusionAICategory, FitFusionAIProduct

@admin.register(FitFusionAICategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('fitfusionai_category_id', 'fitfusionai_category_name', 'fitfusionai_category_isactive', 'fitfusionai_category_ispopular', 'fitfusionai_category_istrending', 'fitfusionai_category_isnewarrival')
    list_filter = ('fitfusionai_category_isactive', 'fitfusionai_category_ispopular', 'fitfusionai_category_istrending', 'fitfusionai_category_isnewarrival')
    search_fields = ('fitfusionai_category_name',)

@admin.register(FitFusionAIProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('fitfusionai_product_id', 'fitfusionai_product_name', 'fitfusionai_category_id', 'fitfusionai_product_price', 'fitfusionai_product_stock', 'fitfusionai_product_active', 'fitfusionai_product_popular', 'fitfusionai_product_trending', 'fitfusionai_product_newarrival')
    list_filter = ('fitfusionai_product_active', 'fitfusionai_product_popular', 'fitfusionai_product_trending', 'fitfusionai_product_newarrival', 'fitfusionai_category_id')  # ✅ Use correct FK field
    search_fields = ('fitfusionai_product_name',)
