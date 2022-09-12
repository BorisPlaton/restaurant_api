from rest_framework import serializers


class Item(serializers.Serializer):
    """An item that is ordered."""
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.IntegerField()


class Client(serializers.Serializer):
    """The client of the order."""
    name = serializers.CharField()
    phone = serializers.CharField()


class Order(serializers.Serializer):
    """
    Client's order. Contains a client information, and the list
    of items.
    """
    id = serializers.IntegerField()
    items = Item(many=True)
    price = serializers.IntegerField()
    address = serializers.CharField()
    client = Client()
    point_id = serializers.CharField()
