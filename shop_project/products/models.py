from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Модель для представления категории товаров.

    Attributes:
        name (str): Название категории.
        slug (str): URL версия названия.
        image (ImageField): Изображение категории.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/')

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для автоматического создания slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Subcategory(models.Model):
    """
    Модель для представления подкатегории товаров.

    Attributes:
        name (str): Название подкатегории.
        slug (str): URL версия названия.
        image (ImageField): Изображение подкатегории.
        category (ForeignKey): Связь с родительской категорией.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='subcategories/')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='subcategories')

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для автоматического создания slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Модель для представления продукта.

    Attributes:
        name (str): Название продукта.
        slug (str): URL версия названия.
        subcategory (ForeignKey): Связь с подкатегорией.
        price (DecimalField): Цена продукта.
        image_small (ImageField): Малое изображение продукта.
        image_medium (ImageField): Среднее изображение продукта.
        image_large (ImageField): Большое изображение продукта.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    subcategory = models.ForeignKey(Subcategory,
                                    on_delete=models.CASCADE,
                                    related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_small = models.ImageField(upload_to='products/small/')
    image_medium = models.ImageField(upload_to='products/medium/')
    image_large = models.ImageField(upload_to='products/large/')

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для автоматического создания slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
