from rest_framework import generics

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryList(generics.ListAPIView):
    """API view для получения списка всех категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductList(generics.ListAPIView):
    """API view для получения списка всех продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
