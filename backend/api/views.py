from django.db.models import Count, Sum
from rest_framework import viewsets
from rest_framework import filters, permissions

from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter, FilterSet

from rest_framework.pagination import PageNumberPagination
from .models import Sale
from rest_framework.response import Response

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from backend.api.serializers import FeeSerializer, OrdersSerializer, ProductUpdateSerializer, ProductsSerializer, SalesSerializer, StockSerializer, TokenSerializer
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
                        # Order.objects.all(), value),
                        Order.objects.filter(
                            is_cancel=0), value),
                ),
                Prefetch(
                    'sales',
                    DateRangeFilter(field_name='date').filter(
                        # Sale.objects.filter(quantity__gt=0), value),
                        Sale.objects.all(), value),
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
                # Prefetch(
                #     'sales',
                #     DateRangeFilter(field_name='date').filter(
                #         Sale.objects.filter(
                #             quantity__lt=0), value),
                #     'returns'
                # ),
                Prefetch(
                    'orders',
                    DateRangeFilter(field_name='date').filter(
                        Order.objects.filter(
                            is_cancel=1), value),
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

    def list(self, request):
        qs = Token.objects.filter(user=request.user).first()
        serializer = TokenSerializer(qs)
        return Response(serializer.data)


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
        Prefetch(
            'sales',
            Sale.objects.all()
        ),
        Prefetch(
            'stocks',
            Stock.objects.filter(
                quantity__gt=0)
        ),
        Prefetch(
            'orders',
            Order.objects.filter(
                is_cancel=0)
        ),
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    # def get_queryset(self):
    #     return super().get_queryset().filter(user=self.request.user)

    # permission_classes = (permissions.IsAuthenticated,)

    # pagination_class = LargeResultsSetPagination
    # def get_queryset(self):
    # return super().get_queryset().filter(user=self.request.user)


class ProductUpdateViewsSet(viewsets.ModelViewSet):

    serializer_class = ProductUpdateSerializer
    queryset = Product.objects.all()


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    pagination_class = LargeResultsSetPagination


class FeeViewSet(viewsets.ModelViewSet):
    serializer_class = FeeSerializer
    queryset = Fee.objects.all()
    # pagination_class = LargeResultsSetPagination
