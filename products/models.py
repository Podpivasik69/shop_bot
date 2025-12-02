# products/models.py
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('preorder', 'Предзаказ'),
        ('in_stock', 'Есть на складе'),
    ]
    name = models.CharField("Название", max_length=200)  # Название (обязательно)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=0)  # Цена (обязательно)
    condition = models.CharField("Состояние", max_length=100)  # Состояние (обязательно) - менеджер пишет сам
    size = models.CharField("Размер", max_length=50)  # Размер (обязательно) - менеджер пишет сам
    description = models.TextField("Описание", blank=True)  # Описание (не обязательно)
    main_image = models.ImageField("Основное фото", upload_to='products/')  # Основное фото (обязательно)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    in_stock = models.BooleanField("В наличии", default=True)

    availability_type = models.CharField(
        "Тип наличия",
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='preorder'
    )
    stock_quantity = models.IntegerField("Количество на складе", default=0, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/gallery/')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фотографии товаров'
        ordering = ['order']
