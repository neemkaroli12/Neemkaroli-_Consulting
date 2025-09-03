from django.contrib import admin
from .models import BlogPost, Product, Module, CompanyType, Estimate
# Register your models here.
admin.site.register(BlogPost)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product')
    list_filter = ('product',)
    search_fields = ('name',)


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'email', 'product')
    list_filter = ('product', 'type')
    search_fields = ('name', 'company_name', 'email')
