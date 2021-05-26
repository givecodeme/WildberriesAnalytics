from django.contrib import admin
from django.urls import path, include
from .api.views import index_view, SalesViewSet, add_sales
from backend.api.views import OrdersViewSet, ProductsViewSet, StockViewSet, add_orders, add_products, add_stocks

import debug_toolbar


urlpatterns = [
    path('', index_view, name='index'),

    path('__debug__/', include(debug_toolbar.urls)),

    path('api/admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
]
