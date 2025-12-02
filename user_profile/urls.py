# user_profile/urls.py
from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile_view, name='profile'),
path('api/telegram-user/', views.telegram_user_api, name='telegram_user_api'),

]
