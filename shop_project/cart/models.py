from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CartItem(models.Model):
    """
    Модель для представления товара в корзине.

    Attributes:
        user (ForeignKey): Связь с пользователем.
        product (ForeignKey): Связь с продуктом.
        quantity (int): Количество товара в корзине.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
