from django.db.models import fields
from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    deals = serializers.FileField(required=True)

    def validate_deals(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('The format of the uploaded file is not ".csv"')
        return value


class CustomersTopSerializer(serializers.Serializer):
    username = serializers.CharField()
    spent_money = serializers.IntegerField()
    gems = serializers.ListField()

