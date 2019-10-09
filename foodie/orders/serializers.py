from rest_framework import serializers

from .models import Product, Order, Item


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price')
        read_only_fields = ('shop',)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered')
        read_only_fields = ('client_user', 'date_time_ordered')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'order', 'quantity', 'notes', 'product')
