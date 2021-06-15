from django.contrib import admin
from django.urls import path, include
from .api.views import index_view, SalesViewSet
from backend.api.views import OrdersViewSet, ProductsViewSet, StockViewSet
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_view, name='index'),

    path('__debug__/', include(debug_toolbar.urls)),

    path('api/admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
