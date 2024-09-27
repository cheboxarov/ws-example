from rest_framework import serializers
from .models import GraphLog


class GraphLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = GraphLog
        fields = "__all__"