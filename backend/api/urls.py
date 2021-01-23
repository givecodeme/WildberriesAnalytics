from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import TodosViewSet

router = DefaultRouter()
router.register('todos', TodosViewSet)

urlpatterns = [
    path('', include(router.urls))
]
