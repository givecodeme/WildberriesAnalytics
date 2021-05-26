from rest_framework import viewsets
from rest_framework import filters
from .models import Todos
from .serializers import TodosSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
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


class TodosViewSet(viewsets.ModelViewSet):
    serializer_class = TodosSerializer
    queryset = Todos.objects.order_by('-id')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = LargeResultsSetPagination
