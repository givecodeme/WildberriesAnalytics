from django.dispatch import receiver
from backend.api.models import Product, Stock, Token
from django.db.models.signals import post_save, pre_save
import requests
from bs4 import BeautifulSoup


@receiver(pre_save, sender=Product)
def pre_save_product(sender, instance, *arggs, **kwargs):
    url = f'https://www.wildberries.ru/catalog/{instance.id}/detail.aspx'
    # url = f'https://www.wildberries.ru/catalog/{instance.id}/detail.aspx'
    data = requests.get(url).content
    soup = BeautifulSoup(data, 'lxml')
    instance.image = soup.find('img', class_='preview-photo').attrs['src']
    instance.name = soup.find('span', class_='name').text


@receiver(post_save, sender=Token)
def post_save_token(sender, instance, *arggs, **kwargs):
    import requests
    token = instance
    url_stocks = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2017-03-25T21:00:00.000Z&key={token.apiKey}'
    data = requests.get(url_stocks).json()

    if Stock.objects.exists() and Product.objects.filter(user__id=token.user_id) or 1:
        for stock in data:
            try:
                stockProd = Stock.objects.get_or_create(
                    name=stock['warehouseName'],
                    product=Product.objects.get_or_create(
                        id=stock['nmId'],
                        subject=stock['subject'],
                        # barcode=stock['barcode'],
                        user=token.user,
                    )[0],
                )[0]
                stockProd.quantity = stock['quantity']
                stockProd.save(update_fields=['quantity'])
            except Exception as e:
                print(e)
    else:
        Stock.objects.bulk_create([
            Stock(
                name=stock['warehouseName'],
                product=Product.objects.get_or_create(
                    id=stock['nmId'],
                    subject=stock['subject'],
                    # barcode=stock['barcode'],
                    user=token.user,
                )[0],
            ) for stock in data
        ])

    print('success')
