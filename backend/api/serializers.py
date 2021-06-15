from rest_framework.serializers import ModelSerializer
from .models import Order, Product, Sale, Stock
from rest_framework import serializers
from backend.api.models import Fee, Token


class SalesSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"


class OrdersSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class StockSerializer(ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'


class FeeSerializer(ModelSerializer):

    class Meta:
        model = Fee
        fields = '__all__'


class StockProductSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ('name', 'quantity')


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('quantity', 'price', 'is_cancel', 'date')


class SaleProductSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = ('quantity', 'price', 'date')


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ('apiKey', 'id', )


class ProductUpdateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductsSerializer(ModelSerializer):
    stocks = StockProductSerializer(many=True)
    # orders = OrderProductSerializer(many=True)
    # sales = SaleProductSerializer(many=True)

    orders_sum = serializers.IntegerField()
    orders_qnt = serializers.IntegerField()

    sales_sum = serializers.IntegerField()
    sales_qnt = serializers.IntegerField()

    stocks_qnt = serializers.IntegerField()

    delivery_sum = serializers.IntegerField()
    com_sum = serializers.IntegerField()

    return_orders = serializers.IntegerField()
    per_sale = serializers.IntegerField()

    return_orders = serializers.IntegerField()

    wb_url = serializers.URLField()

    class Meta:
        model = Product
        fields = '__all__'
