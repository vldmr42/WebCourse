from django.contrib import admin
from .models import Category, Product, City, Supplier


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'get_suppliers_str')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('suppliers')
        return qs

    def city(self, obj):
        return obj.supplier.city

    def get_suppliers_str(self, obj):
        return ', '.join(obj.suppliers.all().values_list('name', flat=True))

    get_suppliers_str.short_description = 'Suppliers'



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(City)
admin.site.register(Supplier)
