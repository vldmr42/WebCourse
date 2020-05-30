from django_rq import job
import requests
from catalog.models import CurrencyRate


@job
def update_currency_rates(self):
    queryset = CurrencyRate.objects.all()
    for rate in queryset:
        pair = f'{rate.currency.upper()}RUB'
        response = requests.get(f'https://www.freeforexapi.com/api/live?pairs={pair}')
        data = response.json()
        try:
            rate.rate = data['rates'][pair]['rate']
            rate.save(update_fields=['rate'])
        except TypeError:
            print('None Error')
            return 'Not updated'

