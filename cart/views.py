from django.shortcuts import render


def cart_view(request):
    """Заглушка для корзины"""
    return render(request, 'cart/stub.html', {
        'title': '🛒 Корзина',
        'message': 'Корзина товаров находится в разработке.',
        'back_url': '/'
    })
