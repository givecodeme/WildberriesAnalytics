from backend.celery import app
from backend.api.models import Product, Stock, Token


@app.task
def create_stocks(token):
    import requests
    url_stocks = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2017-03-25T21:00:00.000Z&key={token.apiKey}'
    data = requests.get(url_stocks).json()

    if Stock.objects.exists():
        for stock in data:
            stockProd = Stock.objects.get_or_create(
                name=stock['warehouseName'],
                product=Product.objects.get_or_create(
                    # subject=stock['subject'],
                    user=token.user,
                    nmid=stock['nmId']
                )[0],
            )[0]
            stockProd.quantity = stock['quantity']
            stockProd.save(update_fields=['quantity'])
    else:
        Stock.objects.bulk_create([
            Stock(
                name=stock['warehouseName'],
                product=Product.objects.get_or_create(
                    # subject=stock['subject'],
                    user=token.user,
                    nmid=stock['nmId']
                )[0],
            ) for stock in data
        ])

    print('success')


def post_save_token(token):
    create_stocks.delay(token)
