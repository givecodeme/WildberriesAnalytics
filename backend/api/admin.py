from django.contrib import admin
from backend.api.models import Product, Token

# Register your models here.


admin.site.register(Token)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['barcode']
    autocomplete_fields = ['user']
