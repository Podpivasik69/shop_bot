# orders/telegram_service.py
import requests
from django.conf import settings


class TelegramNotifier:
    def __init__(self):
        self.bot_token = '8584593593:AAG98u6XBbDV4YxXYvkHiFNwTRf5-TDOawk'
        # self.test_chat_id = '1174231535' # марк
        self.test_chat_id = "1271882788" # я

    def send_order_notification(self, order):
        """Отправка уведомления о новом заказе"""
        message = self._format_order_message(order)
        return self._send_message(message)

    def _format_order_message(self, order):
        # Убираем Markdown разметку для простоты
        return f"""
🛍 НОВЫЙ ЗАКАЗ #{order.id}

📦 Товар: {order.product.name}
💰 Цена: {order.product.price} ₽
📏 Размер: {order.selected_size}
🎯 Состояние: {order.product.condition}

👤 Клиент:
• ФИО: {order.customer_full_name}
• Телефон: {order.phone}
• TG: @{order.tg_username}

📍 Адрес СДЭК:
{order.cdek_address}

💬 Комментарий:
{order.comment if order.comment else 'нет'}

⏰ Создан: {order.created_at.strftime('%d.%m.%Y %H:%M')}
        """.strip()

    def _send_message(self, text):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.test_chat_id,
            'text': text
            # Убрали parse_mode чтобы избежать ошибок форматирования
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False


telegram_notifier = TelegramNotifier()
