from django.db import models
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_size = models.CharField(max_length=50, verbose_name="Выбранный размер")
    customer_full_name = models.CharField(max_length=100, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    cdek_address = models.TextField(verbose_name="Адрес отделения СДЭК")
    tg_username = models.CharField(max_length=100, verbose_name="Ник в Telegram")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} - {self.product.name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
