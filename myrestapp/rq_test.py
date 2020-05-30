# https://www.freeforexapi.com/api/live?pairs=USDRUB
from datetime import datetime, timedelta

import requests
from redis import Redis
from rq import Queue
from rq.decorators import job
from rq_scheduler import Scheduler

redis_conn = Redis()

@job('default', connection=redis_conn)
def get_currency_rate(currency):
    pair = f'{currency}RUB'
    response = requests.get(f'https://www.freeforexapi.com/api/live?pairs={pair}')
    data = response.json()
    try:
        return data['rates'][pair]['rate']
    except TypeError:
        print('NoneType Error')
        return 'Error happened'

scheduler = Scheduler(connection=redis_conn)
# scheduler.enqueue_at(datetime(2020, 5, 30, 20, 15), get_currency_rate, 'USD')
# scheduler.enqueue_in(timedelta(seconds=5), get_currency_rate, 'USD')

get_currency_rate.delay('USD')