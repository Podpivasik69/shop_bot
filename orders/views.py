# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from products.models import Product
from .forms import OrderForm
from .models import Order
from .telegram_service import telegram_notifier  # импортируем сервис


def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # НОВАЯ ПРОВЕРКА: если товар на складе и количество 0
    if product.availability_type == 'in_stock' and product.stock_quantity <= 0:
        messages.error(request, 'Этот товар закончился на складе. Доступен предзаказ.')
        return redirect('products:catalog')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product

            # НОВОЕ: Списание со склада
            if product.availability_type == 'in_stock' and product.stock_quantity > 0:
                product.stock_quantity -= 1
                product.save()

            order.save()

            # ✅ ОТПРАВКА УВЕДОМЛЕНИЯ В TELEGRAM
            telegram_sent = telegram_notifier.send_order_notification(order)
            if telegram_sent:
                messages.success(request, 'Заказ успешно оформлен! Мы свяжемся с вами в Telegram.')
            else:
                messages.warning(request,
                                 'Заказ оформлен, но возникла проблема с уведомлением. Мы свяжемся с вами позже.')

            return redirect('orders:order_success', order_id=order.id)
    else:
        initial = {}
        if request.GET.get('tg_user'):
            initial['tg_username'] = request.GET.get('tg_user')

        form = OrderForm(initial=initial)

    return render(request, 'orders/create_order.html', {
        'form': form,
        'product': product
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


def my_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})
