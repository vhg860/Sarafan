from rest_framework import serializers

from .models import Category, Subcategory, Product


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели подкатегории товаров."""

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category. Включает связанные подкатегории."""
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели продукта.
    Включает информацию о категории, подкатегории и изображениях продукта.
    """
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'subcategory', 'price', 'images'
        ]

    def get_category(self, obj):
        """Возвращает название категории продукта."""
        return obj.subcategory.category.name

    def get_subcategory(self, obj):
        """Возвращает название подкатегории продукта."""
        return obj.subcategory.name

    def get_images(self, obj):
        """Возвращает словарь с URL изображений продукта разных размеров."""
        return {
            'small': obj.image_small.url,
            'medium': obj.image_medium.url,
            'large': obj.image_large.url,
        }
