from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
from django.db.models import Q, Sum
from django.db.models.signals import pre_save
from bs4 import BeautifulSoup
import requests


def pre_save_product(sender, instance, *arggs, **kwargs):
    url = f'https://www.wildberries.ru/catalog/{instance.nmid}/detail.aspx'
    data = requests.get(url).content
    soup = BeautifulSoup(data, 'lxml')
    instance.image = soup.find('img', class_='preview-photo').attrs['src']


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

    # @property
    # def sum(self):
    #     return Decimal(self.quantity * self.price)


class Product(models.Model):
    subject = models.CharField(max_length=50)
    # category =
    nmid = models.IntegerField(unique=True, db_index=True)
    # brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    image = models.URLField(max_length=200, blank=True, null=True)
    sebes = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    # user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def orders_sum(self):
        return sum(map(lambda order: order.quantity * order.price, self.orders.all()))

    def orders_qnt(self):
        return sum(map(lambda order: order.quantity, self.orders.all()))

    def sales_sum(self):
        return sum(map(lambda sale: sale.quantity * sale.price, self.sales.all()))

    def sales_qnt(self):
        return abs(sum(map(lambda sale: sale.quantity, self.sales.all())))

    def stocks_qnt(self):
        return sum(map(lambda stock: stock.quantity, self.stocks.all()))

    def delivery_sum(self):
        return sum(map(lambda delivery: delivery.delivery, self.delivery_set))

    def com_sum(self):
        return sum(map(lambda com: com.commission, self.com_set))

    def return_sum(self):
        return abs(sum(map(lambda ret: ret.quantity, self.returns)))

    def return_orders(self):
        return abs(sum(map(lambda ret: ret.quantity, self.ret_orders)))

    def per_sale(self):
        if self.sales_qnt() == 0:
            return 0
        if self.return_orders():
            return 100 - self.return_orders() / self.sales_qnt() * 100
        return 100

    def wb_url(self):
        return f"https://www.wildberries.ru/catalog/{self.nmid}/detail.aspx"


pre_save.connect(pre_save_product, sender=Product)


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

    # class Meta:


class Token(models.Model):
    apiKey = models.TextField()
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
