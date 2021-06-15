from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
from django.db.models import Q, Sum
from django.db.models.signals import pre_save, post_save
from bs4 import BeautifulSoup
import requests


class Sale(models.Model):

    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # priceWithDisc
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='sales')

    date = models.DateTimeField()

    odid = models.IntegerField()

    class Meta:
        verbose_name = ("Sale")

        verbose_name_plural = ("Sales")

    def sum(self):
        return Decimal(self.quantity * self.price)


class Order(models.Model):

    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # priceWithDisc
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name='orders')
    is_cancel = models.BooleanField(null=True, blank=True)  # 1 - Отмена
    sebes = models.IntegerField(null=True, blank=True)

    date = models.DateTimeField()

    odid = models.IntegerField()

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")


class Product(models.Model):
    subject = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    # category =
    # nmid = models.IntegerField(unique=True, db_index=True)
    # brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    image = models.URLField(max_length=200, blank=True, null=True)
    sebes = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    barcode = models.CharField(max_length=50)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def orders_sum(self):
        return sum([order.price for order in self.orders.all()])

    def orders_qnt(self):
        return sum([order.quantity for order in self.orders.all()])

    def sales_sum(self):
        return sum([sale.price for sale in self.sales.all()])

    def sales_qnt(self):
        return sum([sale.quantity for sale in self.sales.all()])

    def stocks_qnt(self):
        return sum([stock.quantity for stock in self.stocks.all()])

    def delivery_sum(self):
        return sum([delivery.delivery for delivery in self.delivery_set])

    def com_sum(self):
        return sum([com.commission for com in self.com_set])

    # def return_sales(self):
    #     return abs(sum(map(lambda ret: ret.quantity, self.returns)))

    def return_orders(self):
        return abs(sum(map(lambda ret: ret.quantity, self.ret_orders)))

    def per_sale(self):
        # if self.sales_qnt() == 0:
        #     return 0
        if self.return_orders():
            return 100 - self.return_orders() / self.orders_qnt() * 100 if self.orders_qnt() else 0
        return 100

    def wb_url(self):
        return f"https://www.wildberries.ru/catalog/{self.id}/detail.aspx"


class Stock(models.Model):

    name = models.CharField(max_length=50)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(blank=True, null=True)
    # quantityFull = models.IntegerField()
    # quantityNotInOrders = models.IntegerField()

    class Meta:
        verbose_name = ("Stock")
        verbose_name_plural = ("Stocks")

    def __str__(self):
        return self.name


class Fee(models.Model):
    name = models.CharField(max_length=50)

    delivery = models.IntegerField(default=0)  # delivery_rub

    commission = models.DecimalField(default=0,
                                     max_digits=7, decimal_places=2)  # retail_commission
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE)

    date = models.DateTimeField()


class Token(models.Model):
    apiKey = models.TextField()
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE)
