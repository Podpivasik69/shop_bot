from django.shortcuts import render


def profile_view(request):
    """Заглушка для профиля"""
    return render(request, 'profile/stub.html', {
        'title': '👤 Профиль',
        'message': 'Раздел профиля находится в разработке.',
        'back_url': '/'
    })
