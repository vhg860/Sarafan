from products.models import Product
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления корзиной пользователя.

    Предоставляет операции CRUD для товаров в корзине, а также
    дополнительные действия для просмотра и очистки корзины.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает queryset товаров в корзине текущего пользователя."""
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request):
        """Создает новый товар в корзине или обновляет его количество."""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Обновляет количество товара в корзине."""
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'},
                            status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def view_cart(self, request):
        """Возвращает содержимое корзины с количеством товаров и суммой."""
        cart_items = self.get_queryset()
        total_items = sum(
            item.quantity for item in cart_items
        )
        total_price = sum(
            item.product.price * item.quantity for item in cart_items
        )

        serializer = CartSerializer({
            'items': cart_items,
            'total_items': total_items,
            'total_price': total_price
        })
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def clear_cart(self, request):
        """Очищает корзину пользователя."""
        self.get_queryset().delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)
