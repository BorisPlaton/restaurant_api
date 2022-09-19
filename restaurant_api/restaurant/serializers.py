from rest_framework import serializers

from restaurant.models import Check


class Item(serializers.Serializer):
    """An ordered item."""
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.IntegerField()


class Client(serializers.Serializer):
    """A client of order."""
    name = serializers.CharField()
    phone = serializers.CharField()


class Order(serializers.Serializer):
    """
    Client's order. Contains client information, and a list
    of items.
    """
    id = serializers.IntegerField()
    items = Item(many=True)
    price = serializers.IntegerField()
    address = serializers.CharField()
    client = Client()
    point_id = serializers.CharField()


class CheckSerializer(serializers.ModelSerializer):
    """The order check with only its id field."""

    class Meta:
        model = Check
        fields = ['id']
