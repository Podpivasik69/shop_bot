from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from orders.models import Order


def catalog(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()

    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, in_stock=True)
    else:
        products = Product.objects.filter(in_stock=True)
    orders_count = Order.objects.count()
    return render(request, 'products/catalog.html', {
        'categories': categories,
        'products': products,
        'active_category': category_slug,
        'orders_count': orders_count
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })
