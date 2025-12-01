document.addEventListener('DOMContentLoaded', function() {
    // Можно добавить валидацию форм, маски для телефона и т.д.
    console.log('Order form loaded');

    // Пример: Маска для телефона
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = '+7 (' + value;
                if (value.length > 7) value = value.slice(0, 7) + ') ' + value.slice(7);
                if (value.length > 12) value = value.slice(0, 12) + '-' + value.slice(12);
                if (value.length > 15) value = value.slice(0, 15) + '-' + value.slice(15, 17);
            }
            e.target.value = value;
        });
    }
});