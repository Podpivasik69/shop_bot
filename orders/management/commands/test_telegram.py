# orders/management/commands/test_telegram.py
from django.core.management.base import BaseCommand
from orders.models import Order
from orders.telegram_service import telegram_notifier


class Command(BaseCommand):
    help = 'Test Telegram notifications'

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='Order ID to test')

    def handle(self, *args, **options):
        order_id = options['order_id']
        try:
            order = Order.objects.get(id=order_id)
            success = telegram_notifier.send_order_notification(order)

            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Telegram notification sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to send Telegram notification')
                )

        except Order.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Order with id {order_id} does not exist')
            )