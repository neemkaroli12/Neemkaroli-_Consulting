from django.contrib import admin
from .models import BlogPost, Product, Module, CompanyType, Estimate,SubModule,SubSubModule
# Register your models here.
admin.site.register(BlogPost)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "name", 
        "product", 
        "technical_days", 
        "functional_days", 
       
    )
    search_fields = ("name", "product__name")
    list_filter = ("product",)

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'email', 'product')
    list_filter = ('product', 'type')
    search_fields = ('name', 'company_name', 'email')
    
@admin.register(SubModule)
class SubModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "module", "get_product")
    search_fields = ("name", "module__name", "module__product__name")
    list_filter = ("module__product",)

    def get_product(self, obj):
        return obj.module.product.name if obj.module and obj.module.product else "-"
    get_product.short_description = "Product"
    
    
@admin.register(SubSubModule)
class SubSubModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "submodule", "get_module", "get_product")
    search_fields = ("name", "submodule__name", "submodule__module__name")
    list_filter = ("submodule__module__product",)

    def get_module(self, obj):
        return obj.submodule.module.name if obj.submodule and obj.submodule.module else "-"
    get_module.short_description = "Module"

    def get_product(self, obj):
        return obj.submodule.module.product.name if obj.submodule and obj.submodule.module and obj.submodule.module.product else "-"
    get_product.short_description = "Product"