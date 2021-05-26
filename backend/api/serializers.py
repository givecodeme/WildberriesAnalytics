
from rest_framework.serializers import ModelSerializer
from .models import Todos


class TodosSerializer(ModelSerializer):
    class Meta:
        model = Todos
        fields = ('id', 'title', 'completed')
