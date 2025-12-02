# user_profile/views.py
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TelegramUser

def profile_view(request):
    """Заглушка для профиля"""
    return render(request, 'user_profile/stub.html', {
        'title': '👤 Профиль',
        'message': 'Раздел профиля находится в разработке.',
        'back_url': '/'
    })


# НОВАЯ ФУНКЦИЯ (которую вы добавили)
@csrf_exempt
def telegram_user_api(request):
    """
    API endpoint для получения данных пользователя Telegram
    Вызывается из JavaScript в base.html
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        # Парсим JSON данные
        data = json.loads(request.body.decode('utf-8'))
        telegram_id = data.get('telegram_id')

        if not telegram_id:
            return JsonResponse({'error': 'telegram_id is required'}, status=400)

        # Создаем или обновляем пользователя
        user, created = TelegramUser.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': data.get('username', '')[:100],
                'first_name': data.get('first_name', '')[:100],
                'last_name': data.get('last_name', '')[:100],
                'photo_url': data.get('photo_url', '')[:500],
                'is_synced': True,
            }
        )

        # Сохраняем telegram_id в сессии
        request.session['telegram_id'] = telegram_id
        request.session['telegram_user_id'] = user.id  # ID из БД

        return JsonResponse({
            'success': True,
            'created': created,
            'user_id': user.id,
            'display_name': user.get_display_name()
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
