from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework import routers

from .views import (
    index_view, SalesViewSet, add_sales,
    OrdersViewSet, ProductsViewSet,
    StockViewSet, add_orders, add_products, add_stocks
)
from backend.api.views import FeeViewSet, TokenViewSet, add_comission
router = routers.DefaultRouter()
router.register('sales', SalesViewSet)
router.register('orders', OrdersViewSet)
router.register('products', ProductsViewSet)
router.register('stocks', StockViewSet)
router.register('fees', FeeViewSet)
router.register('tokens', TokenViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('add_sales', add_sales,),
    path('add_orders', add_orders,),
    path('add_prod', add_products,),
    path('add_stocks', add_stocks,),
    path('add_com', add_comission),

    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]
