from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework import routers

from .views import (
    index_view, SalesViewSet,
    OrdersViewSet, ProductsViewSet,
    StockViewSet,
)
from backend.api.views import FeeViewSet, ProductUpdateViewsSet, TokenViewSet
router = routers.DefaultRouter()
router.register('sales', SalesViewSet)
router.register('orders', OrdersViewSet)
router.register('products', ProductsViewSet)
router.register('product_update', ProductUpdateViewsSet)
router.register('stocks', StockViewSet)
router.register('fees', FeeViewSet)
router.register('tokens', TokenViewSet)


urlpatterns = [
    path('', include(router.urls)),


    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]
