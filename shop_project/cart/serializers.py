from products.serializers import ProductSerializer
from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для модели товара в корзине."""
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.Serializer):
    """Сериализатор для представления корзины."""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
