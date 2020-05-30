import requests
from django.contrib import admin
from django.db.models import Prefetch

from .models import Category, Product, City, Supplier, CurrencyRate


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'suppliers',
        # 'city',
        # 'get_categories_str',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        prefetch_qs = Category.objects.only('name')
        prefetch = Prefetch('category', queryset=prefetch_qs)

        qs = qs.prefetch_related(prefetch)
        return qs

    # def city(self, obj):
    #     return obj.suppliers.city

    # def get_categories_str(self, obj):
        # return ', '.join([c.name for c in obj.category.all()])
        # return ', '.join(obj.category.all().values_list('name', flat=True))

    # get_categories_str.short_description = 'Category'

    # def get_suppliers_str(self, obj):
    #     return ', '.join(obj.suppliers.all().values_list('name', flat=True))

    # get_suppliers_str.short_description = 'Suppliers'

class CurrencyRateAdmin(admin.ModelAdmin):

    actions = ['update_currency_rates']

    def update_currency_rates(self, request, queryset):
        for rate in queryset:
            pair = f'{rate.currency.upper()}RUB'
            response = requests.get(f'https://www.freeforexapi.com/api/live?pairs={pair}')
            data = response.json()
            try:
                rate.rate = data['rates'][pair]['rate']
                rate.save(update_fields=['rate'])
            except TypeError:
                pass



admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(City)
admin.site.register(Supplier)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
