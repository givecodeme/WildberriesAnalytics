from django.db.models import Count, Sum
from rest_framework import viewsets
from rest_framework import filters, permissions

from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter, FilterSet

from rest_framework.pagination import PageNumberPagination
from .models import Sale
from rest_framework.response import Response

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from backend.api.serializers import FeeSerializer, OrdersSerializer, ProductsSerializer, SalesSerializer, StockSerializer, TokenSerializer
import requests
from django.http.response import HttpResponse
from backend.api.models import Fee, Order, Product, Stock, Token
from django_filters.rest_framework.filters import DateFromToRangeFilter, DateRangeFilter
from django.db.models import Max, Min, Prefetch
import time
# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class ProductFilter(FilterSet):
    date = DateRangeFilter(method='range_date')

    def range_date(self, qs, name, value):
        if value:
            return qs.prefetch_related(None).prefetch_related(
                Prefetch(
                    'orders',
                    DateRangeFilter(field_name='date').filter(
                        Order.objects.all(), value),
                    # filter(is_cancel=1)
                ),
                Prefetch(
                    'sales',
                    DateRangeFilter(field_name='date').filter(
                        Sale.objects.all(), value),
                    # filter(quantity__gt=0)
                ),
                Prefetch(
                    'stocks',
                    Stock.objects.filter(quantity__gt=0)
                ),
                Prefetch(
                    'fee_set',
                    DateRangeFilter(field_name='date').filter(
                        Fee.objects.filter(
                            name='Логистика'), value),
                    'delivery_set'
                ),
                Prefetch(
                    'fee_set',
                    DateRangeFilter(field_name='date').filter(
                        Fee.objects.filter(
                            name='Продажа'), value),
                    'com_set'
                ),
                Prefetch(
                    'sales',
                    DateRangeFilter(field_name='date').filter(
                        Sale.objects.filter(
                            quantity__lt=0), value),
                    'returns'
                ),
                Prefetch(
                    'orders',
                    DateRangeFilter(field_name='date').filter(
                        Order.objects.filter(is_cancel=1), value),
                    'ret_orders'
                ),
                # Prefetch(
                #     'orders',
                #     DateRangeFilter(field_name='date').filter(
                #         Order.objects.filter(is_cancel=1), value),
                #     'returns'
                # )
            )
            # .order_by('-sales__price')
            # .annotate( sum_orders=Sum('orders__price'))
            # .order_by('-stocks__quantity')

    class Meta:
        model = Product
        fields = ['date']


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },

            'count': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'results': data
        })


class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SalesViewSet(viewsets.ModelViewSet):
    serializer_class = SalesSerializer
    queryset = Sale.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ['category', 'in_stock']

    # search_fields = ('title',)
    pagination_class = LargeResultsSetPagination


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrdersSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_cancel',)

    # filter_backends = (filters.bac,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('title',)
    pagination_class = LargeResultsSetPagination


class ProductsViewSet(viewsets.ModelViewSet):

    serializer_class = ProductsSerializer
    queryset = Product.objects.prefetch_related(
        Prefetch('stocks', Stock.objects.filter(quantity__gt=0)),
        # 'stocks',
        'orders', 'sales',
        Prefetch(
            'fee_set',

            Fee.objects.filter(
                name='Логистика'),
            'delivery_set'
        ),
        Prefetch(
            'fee_set',
            Fee.objects.filter(
                name='Продажа'),
            'com_set'
        ),


        Prefetch(
            'sales',

            Sale.objects.filter(
                quantity__lt=0),
            'returns'
        ),
        Prefetch(
            'orders',
            Order.objects.filter(is_cancel=1),
            'ret_orders'
        ),
    )
    filter_backends = (
        DjangoFilterBackend,
        #    filters.OrderingFilter,
    )
    # filterset_fields = ('sales_sum', 'price', )
    # ordering_fields = ('sales_sum', "orders_sum")
    filterset_class = ProductFilter
    # pagination_class = LargeResultsSetPagination
    # permission_classes = (permissions.IsAuthenticated,)

    # def get_queryset(self):
    # return super().get_queryset().filter(user=self.request.user)


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    pagination_class = LargeResultsSetPagination


class FeeViewSet(viewsets.ModelViewSet):
    serializer_class = FeeSerializer
    queryset = Fee.objects.all()
    # pagination_class = LargeResultsSetPagination


def add_sales(request):
    url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/sales?dateFrom=2017-03-25T21:00:00.000Z&key=YWE3YzFlNWItOWVhZS00OWJiLWJhODQtMDA0N2E0MzFhMWMw'
    data = requests.get(url).json()
    sales = []
    if Sale.objects.exists():
        for sale in data:
            try:
                sale, created = Sale.objects.get_or_create(
                    product=Product.objects.get_or_create(
                        nmid=sale['nmId'],
                        subject=sale['subject']
                    )[0],
                    price=int(sale['priceWithDisc']),
                    quantity=sale['quantity'],
                    date=sale['date'],
                    odid=sale['odid']
                )
            except:
                pass
            # if not created:
            #     break

    else:
        Sale.objects.bulk_create([
            Sale(
                product=Product.objects.get_or_create(
                    nmid=sale['nmId'],
                    # subject=sale['subject']
                )[0],
                price=int(sale['priceWithDisc']),
                quantity=sale['quantity'],
                date=sale['date'],
                odid=sale['odid']
            ) for sale in data]
        )

    return HttpResponse('success')


def add_orders(request):
    url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders?dateFrom=2017-02-20&flag=0&key=YWE3YzFlNWItOWVhZS00OWJiLWJhODQtMDA0N2E0MzFhMWMw'
    data = requests.get(url).json()[::-1]
    if Order.objects.exists():
        for sale in data:
            order, created = Order.objects.get_or_create(
                quantity=sale['quantity'],
                price=int(sale['totalPrice']) *
                (100-int(sale['discountPercent']))/100,
                product=Product.objects.get_or_create(
                    nmid=sale['nmId'],
                    subject=sale['subject']
                )[0],
                date=sale['date'],
                odid=sale['odid'],
            )

            if order.is_cancel != sale['isCancel']:
                order.is_cancel = 1 if sale['isCancel'] else 0
                order.save(update_fields=['is_cancel'])
            # if not created:
            #     break

    else:
        Order.objects.bulk_create([
            Order(
                quantity=sale['quantity'],
                price=sale['totalPrice'] *
                (100-sale['discountPercent'])/100,
                product=Product.objects.get_or_create(
                    nmid=sale['nmId'],
                    # subject=sale['subject']
                )[0],
                date=sale['date'],
                odid=sale['odid'],
                is_cancel=1 if sale['isCancel'] else 0
            ) for sale in data]
        )

    return HttpResponse('success')


def add_products(req):

    from bs4 import BeautifulSoup

    url_stocks = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2017-03-25T21:00:00.000Z&key=YWE3YzFlNWItOWVhZS00OWJiLWJhODQtMDA0N2E0MzFhMWMw'
    stocks = requests.get(url_stocks).json()
    prods = []
    created = []

    if not Product.objects.exists():
        for stock in stocks:
            if stock['nmId'] in created:
                continue
            url = f'https://www.wildberries.ru/catalog/{stock["nmId"]}/detail.aspx'
            data = requests.get(url).content
            soup = BeautifulSoup(data, 'lxml')

            prods.append(
                Product(
                    subject=stock['subject'],
                    nmid=stock['nmId'],
                    image=soup.find('img', class_='preview-photo').attrs['src']
                ))
            created.append(stock['nmId'])
            # time.sleep(1)
        Product.objects.bulk_create(prods)
    else:
        for stock in stocks:
            if Product.objects.filter(
                nmid=stock['nmId'],
                subject=stock['subject']
            ).exists():
                continue

            url = f'https://www.wildberries.ru/catalog/{stock["nmId"]}/detail.aspx'
            data = requests.get(url).content
            soup = BeautifulSoup(data, 'lxml')

            prod = Product.objects.get_or_create(
                nmid=stock['nmId'],
            )[0]
            prod.subject = stock['subject']
            prod.image = soup.find(
                'img', class_='preview-photo').attrs['src'],
            prod.save(update_fields=['image', 'subject'])
            time.sleep(1)

    return HttpResponse('success')


def add_stocks(request):

    url_stocks = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2017-03-25T21:00:00.000Z&key=YWE3YzFlNWItOWVhZS00OWJiLWJhODQtMDA0N2E0MzFhMWMw'
    data = requests.get(url_stocks).json()

    for stock in data:
        stockProd = Stock.objects.get_or_create(
            name=stock['warehouseName'],
            product=Product.objects.get_or_create(nmid=stock['nmId'])[0]
        )[0]
        stockProd.quantity = stock['quantity']
        stockProd.save(update_fields=['quantity'])

    # Stock.objects.bulk_create([
    #     Stock(
    #         name=stock['warehouseName'],
    #         quantity=stock['quantity'],
    #         product=Product.objects.get(nmid=stock['nmId'])
    #         # quantityFull=stock['quantityFull'],
    #         # quantityNotInOrders=stock['quantityNotInOrders'],
    #     )
    #     for stock in data
    # ])

    return HttpResponse('success')


# def add_delivery(req):
#     url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod?dateFrom=2020-06-01&key=YWE3YzFlNWItOWVhZS00OWJiLWJhODQtMDA0N2E0MzFhMWMw&limit=1000&rrdid=0&dateto=2021-06-30'
#     data = requests.get(url).json()

#     if Delivery.objects.exists():
#         pass
#     else:
#         Delivery.objects.bulk_create([
#             Delivery(
#                 price=delivery['delivery_rub'],
#                 product=Product.objects.get(nmid=delivery['nm_id']),
#                 date=delivery['sale_dt']
#             )
#             for delivery in data if delivery['supplier_oper_name'] == 'Логистика'
#         ])
#     return HttpResponse('success')


def add_comission(req):
    url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod?dateFrom=2020-06-01&key=YWE3YzFlNWItOWVhZS00OWJiLWJhODQtMDA0N2E0MzFhMWMw&limit=1000&rrdid=0&dateto=2021-06-30'
    data = requests.get(url).json()

    if Fee.objects.exists():
        for delivery in data:
            fe, created = Fee.objects.get_or_create(
                name=delivery['supplier_oper_name'],
                delivery=delivery['delivery_rub'],
                commission=delivery['retail_commission'],
                product=Product.objects.get_or_create(
                    nmid=delivery['nm_id'])[0],
                date=delivery['order_dt']
            )
    else:
        Fee.objects.bulk_create([
            Fee(
                name=delivery['supplier_oper_name'],
                delivery=delivery['delivery_rub'],
                commission=delivery['retail_commission'],
                product=Product.objects.get_or_create(
                    nmid=delivery['nm_id'])[0],
                date=delivery['order_dt']
            )
            for delivery in data
        ])

    return HttpResponse('success')
