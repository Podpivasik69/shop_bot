# orders/management/commands/debug_telegram.py
from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Debug Telegram connection'

    def handle(self, *args, **options):
        bot_token = '8584593593:AAG98u6XBbDV4YxXYvkHiFNwTRf5-TDOawk'
        chat_id = '1271882788'

        # Простое сообщение
        message = "🔧 Тестовое сообщение от бота"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }

        try:
            self.stdout.write(f"Отправляем сообщение на chat_id: {chat_id}")
            response = requests.post(url, json=payload, timeout=10)
            self.stdout.write(f"Status Code: {response.status_code}")
            self.stdout.write(f"Response: {response.text}")

            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ Сообщение отправлено!'))
            else:
                self.stdout.write(self.style.ERROR('❌ Ошибка отправки'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Исключение: {e}'))