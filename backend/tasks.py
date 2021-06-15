# from celery.schedules import crontab
# from time import sleep
import requests
from backend.celery import app
# from _datetime import timedelta
from celery.schedules import crontab
# from celery import Celery
from backend.api.models import Product, Stock, Token


from celery import shared_task
from backend.api.models import Fee, Order, Product, Sale, Stock, Token
import time

# app = Celery('backend')

# @app.task
# def hello_world():
#     sleep(1)  # поставим тут задержку в 10 сек для демонстрации ассинхрности
#     print('Hello World')


# @shared_task
@shared_task
def update_stock():
    print('start')
    for token in Token.objects.iterator():
        url_stocks = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2017-03-25T21:00:00.000Z&key={token.apiKey}'
        data = requests.get(url_stocks).json()

        if Stock.objects.exists():
            for stock in data:
                stockProd = Stock.objects.get_or_create(
                    name=stock['warehouseName'],
                    product=Product.objects.get_or_create(
                        id=stock['nmId'],
                        # barcode=stock['barcode'],
                        subject=stock['subject'],
                        user=token.user,
                    )[0],
                )[0]
                stockProd.quantity = stock['quantity']
                stockProd.save(update_fields=['quantity'])
        else:
            Stock.objects.bulk_create([
                Stock(
                    name=str(stock['warehouseName']),
                    product=Product.objects.get_or_create(
                        id=stock['nmId'],
                        # barcode=stock['barcode'],
                        user=token.user,
                        subject=stock['subject'],
                    )[0],
                ) for stock in data
            ])

    print('success')


@shared_task
def update_sales():
    print('start')
    for token in Token.objects.iterator():

        url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/sales?dateFrom=2017-03-25T21:00:00.000Z&key={token.apiKey}'
        data = requests.get(url).json()[::-1]
        sales = []
        if Sale.objects.exists():
            for sale in data:
                try:
                    sale, created = Sale.objects.get_or_create(
                        # id=sale['odid'],
                        product=Product.objects.get_or_create(
                            id=sale['nmId'],
                            # barcode=sale['barcode'],
                            user=token.user,
                            subject=sale['subject']
                        )[0],
                        price=int(sale['priceWithDisc']),
                        quantity=sale['quantity'],
                        date=sale['date'],
                        odid=sale['odid']
                    )
                    if not created:
                        break
                except Exception as e:
                    print(e)
                    pass

        else:
            Sale.objects.bulk_create([
                Sale(
                    product=Product.objects.get_or_create(
                        id=sale['nmId'],
                        # barcode=sale['barcode'],
                        user=token.user,
                        subject=sale['subject']
                    )[0],
                    price=int(sale['priceWithDisc']),
                    quantity=sale['quantity'],
                    date=sale['date'],
                    odid=sale['odid']
                ) for sale in data]
            )

    print('success')


@shared_task
def update_orders():
    print('start')
    for token in Token.objects.iterator():

        url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders?dateFrom=2017-02-20&flag=0&key={token.apiKey}'
        data = requests.get(url).json()[::-1]
        if Order.objects.exists():
            for sale in data:
                try:
                    order, created = Order.objects.get_or_create(
                        quantity=sale['quantity'],
                        price=sale['totalPrice'] *
                        (100-sale['discountPercent'])/100,
                        product=Product.objects.get_or_create(
                            id=sale['nmId'],
                            # barcode=sale['barcode'],
                            user=token.user,
                            subject=sale['subject']
                        )[0],
                        date=sale['date'],
                        odid=sale['odid'],
                    )

                    if order.is_cancel != sale['isCancel']:
                        order.is_cancel = 1 if sale['isCancel'] else 0
                        order.save(update_fields=['is_cancel'])
                    if not created:
                        break

                except Exception as e:
                    print(e)
        else:
            Order.objects.bulk_create([
                Order(
                    quantity=sale['quantity'],
                    price=sale['totalPrice'] *
                    (100-sale['discountPercent'])/100,
                    product=Product.objects.get_or_create(
                        id=sale['nmId'],
                        # barcode=sale['barcode'],
                        user=token.user,
                        subject=sale['subject']
                    )[0],
                    date=sale['date'],
                    odid=sale['odid'],
                    is_cancel=1 if sale['isCancel'] else 0
                ) for sale in data]
            )

    print('success')


@shared_task
def update_comissions():
    print('start')
    for token in Token.objects.iterator():
        # rrdid = 0
        # url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod?dateFrom=2020-06-01&key={token.apiKey}&limit=10000&rrdid={rrdid}&dateto=2021-06-30'
        data = requests.get('https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod', {
            "dateFrom": "2020-06-01",
            "key": token.apiKey,
            "limit": 10000,
            "rrdid": 0,
            "dateto": "2021-06-30"
        }).json()[::-1]
        # res = requests.get(url).json()
        # data = res
        # while res:
        #     rrdid += 1
        #     url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod?dateFrom=2020-06-01&key={token.apiKey}&limit=10000&rrdid={rrdid}&dateto=2021-06-30'
        #     res = requests.get(url).json()
        #     data += res

        if Fee.objects.exists():
            for delivery in data:
                try:
                    fe, created = Fee.objects.get_or_create(
                        id=delivery['rrd_id'],
                        name=delivery['supplier_oper_name'],
                        delivery=delivery['delivery_rub'],
                        commission=delivery['retail_commission'],
                        product=Product.objects.get_or_create(
                            id=delivery['nm_id'],
                            user=token.user,
                            subject=delivery['subject_name']
                            # barcode=delivery['barcode'],
                        )[0],
                        date=delivery['order_dt']
                    )
                    # if not created:
                    #     break
                except Exception as e:
                    print(e)
        else:
            Fee.objects.bulk_create([
                Fee(
                    id=delivery['rrd_id'],
                    name=delivery['supplier_oper_name'],
                    delivery=delivery['delivery_rub'],
                    commission=delivery['retail_commission'],
                    product=Product.objects.get_or_create(
                        id=delivery['nm_id'],
                        # barcode=delivery['barcode'],
                        subject=delivery['subject_name'],
                        user=token.user,
                    )[0],
                    date=delivery['order_dt']
                )
                for delivery in data
            ])
    print('success')
