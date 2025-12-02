from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'selected_size',
            'customer_full_name',
            'phone',
            'cdek_address',
            'tg_username',
            'comment'
        ]
        widgets = {
            'selected_size': forms.TextInput(attrs={
                'placeholder': 'Например: M или 42',
                'class': 'form-input'
            }),
            'customer_full_name': forms.TextInput(attrs={
                'placeholder': 'Иванов Иван Иванович',
                'class': 'form-input'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (999) 999-99-99',
                'class': 'form-input'
            }),
            'cdek_address': forms.Textarea(attrs={
                'placeholder': 'Город, улица, номер отделения СДЭК',
                'rows': 3,
                'class': 'form-textarea'
            }),
            'tg_username': forms.TextInput(attrs={
                'placeholder': '@username',
                'class': 'form-input'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Дополнительные пожелания',
                'rows': 2,
                'class': 'form-textarea'
            }),
        }

    # НОВЫЙ МЕТОД: настройка поля tg_username в зависимости от контекста
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если поле уже имеет значение (автозаполнено), делаем его readonly
        if self.initial.get('tg_username'):
            self.fields['tg_username'].widget.attrs['readonly'] = True
            self.fields['tg_username'].widget.attrs['title'] = 'Заполнено из вашего профиля Telegram'
