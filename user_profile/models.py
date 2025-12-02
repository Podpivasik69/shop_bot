# user_profile/models.py
from django.db import models


class TelegramUser(models.Model):
    """
    Пользователь Telegram для SKET Shop
    Данные могут быть частично скрыты пользователем в Telegram
    """
    telegram_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ID Telegram пользователя",
        help_text="Уникальный ID пользователя в Telegram (всегда есть)"
    )

    username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Юзернейм в Telegram",
        help_text="@username (может быть скрыт пользователем)"
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Имя",
        help_text="Имя пользователя (может быть скрыто)"
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Фамилия",
        help_text="Фамилия пользователя (может быть скрыта)"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
        help_text="Номер телефона (заполняется при заказе)"
    )

    photo_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на фото профиля",
        help_text="Ссылка на аватарку в Telegram (может быть скрыта)"
    )

    is_synced = models.BooleanField(
        default=False,
        verbose_name="Синхронизирован с Telegram",
        help_text="Пользователь авторизован через Telegram WebApp"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Может ли пользователь совершать покупки"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        """Отображение в админке и консоли"""
        if self.first_name:
            if self.username:
                return f"{self.first_name} (@{self.username})"
            return f"{self.first_name} (#{self.telegram_id})"
        return f"User #{self.telegram_id}"

    def get_display_name(self):
        """Имя для отображения в интерфейсе"""
        if self.first_name:
            return self.first_name
        return f"Покупатель #{self.telegram_id}"

    def has_private_profile(self):
        """Проверка, скрыл ли пользователь данные в Telegram"""
        return not (self.first_name or self.username or self.photo_url)

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
        ordering = ['-created_at']
