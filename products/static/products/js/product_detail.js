// products/static/products/js/product_navigation.js

// ===== НАВИГАЦИЯ МЕЖДУ КАТАЛОГОМ И ТОВАРОМ =====

// Функция для перехода назад с сохранением позиции
function goBackToCatalog(event) {
    if (event) event.preventDefault();

    // Получаем сохраненные данные
    const scrollPosition = sessionStorage.getItem('catalog_scroll') || 0;
    const activeCategory = sessionStorage.getItem('catalog_category') || '';

    // Формируем URL с категорией
    let backUrl = '/';
    if (activeCategory) {
        backUrl = `/?category=${encodeURIComponent(activeCategory)}`;
    }

    // Переходим на каталог
    window.location.href = backUrl;
}

// Сохраняем позицию и категорию ПЕРЕД уходом с каталога на товар
function saveCatalogState() {
    // Сохраняем позицию скролла
    sessionStorage.setItem('catalog_scroll', window.pageYOffset || document.documentElement.scrollTop);

    // Сохраняем активную категорию из URL
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category') || '';
    sessionStorage.setItem('catalog_category', category);
}

// Восстанавливаем позицию при загрузке каталога
function restoreCatalogPosition() {
    const savedScroll = sessionStorage.getItem('catalog_scroll');
    if (savedScroll) {
        // Небольшая задержка для гарантированной загрузки контента
        setTimeout(() => {
            window.scrollTo({
                top: parseInt(savedScroll),
                behavior: 'instant'
            });
        }, 100);
    }
}

// ===== ГАЛЕРЕЯ ТОВАРА =====
function initGallery() {
    const galleryTrack = document.getElementById('gallery-track');
    if (!galleryTrack) return; // Если нет галереи, выходим

    const slides = document.querySelectorAll('.slide');
    const currentSlideElement = document.getElementById('current-slide');
    const totalSlidesElement = document.getElementById('total-slides');

    let currentSlide = 0;
    let startX = 0;
    let currentX = 0;
    let isDragging = false;

    if (totalSlidesElement) {
        totalSlidesElement.textContent = slides.length;
    }

    function updateSlidePosition() {
        galleryTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
        if (currentSlideElement) {
            currentSlideElement.textContent = currentSlide + 1;
        }
    }

    // Обработчики событий
    galleryTrack.addEventListener('mousedown', startDrag);
    galleryTrack.addEventListener('touchstart', startDrag);

    galleryTrack.addEventListener('mousemove', drag);
    galleryTrack.addEventListener('touchmove', drag);

    galleryTrack.addEventListener('mouseup', endDrag);
    galleryTrack.addEventListener('touchend', endDrag);
    galleryTrack.addEventListener('mouseleave', endDrag);

    function startDrag(e) {
        isDragging = true;
        startX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        galleryTrack.style.transition = 'none';
    }

    function endDrag(e) {
        if (!isDragging) return;
        isDragging = false;

        const diff = startX - currentX;
        const threshold = window.innerWidth * 0.1;

        galleryTrack.style.transition = 'transform 0.3s ease-out';

        if (Math.abs(diff) > threshold) {
            if (diff > 0 && currentSlide < slides.length - 1) {
                currentSlide++;
            } else if (diff < 0 && currentSlide > 0) {
                currentSlide--;
            }
        }

        updateSlidePosition();
    }

    function drag(e) {
        if (!isDragging) return;

        e.preventDefault();
        currentX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        const diff = startX - currentX;

        let offset = (currentSlide * 100) + (diff / window.innerWidth * 100);

        // Резиновый эффект на обеих границах
        if (currentSlide === 0 && offset > 0) {
            offset = offset * 0.3;
        } else if (currentSlide === slides.length - 1 && offset < currentSlide * 100) {
            offset = currentSlide * 100 + (offset - currentSlide * 100) * 0.3;
        } else if (offset < 0) {
            offset = offset * 0.3;
        } else if (offset > (slides.length - 1) * 100) {
            const overshoot = offset - (slides.length - 1) * 100;
            offset = (slides.length - 1) * 100 + overshoot * 0.3;
        }

        galleryTrack.style.transform = `translateX(-${offset}%)`;
    }

    // Инициализация галереи
    updateSlidePosition();
}

// ===== ОСНОВНАЯ ИНИЦИАЛИЗАЦИЯ =====
document.addEventListener('DOMContentLoaded', function () {
    // Инициализируем галерею (если на странице товара)
    initGallery();

    // Навигационная логика
    if (window.location.pathname === '/') {
        // Мы на странице каталога
        restoreCatalogPosition();

        // Сохраняем состояние при клике на товар
        document.addEventListener('click', function (e) {
            const productCard = e.target.closest('.product-card.clickable');
            if (productCard) {
                saveCatalogState();
            }
        });
    }

    // Если мы на странице товара - настраиваем кнопку "Назад"
    if (window.location.pathname.includes('/product/')) {
        const backButton = document.getElementById('back-to-catalog');
        if (backButton) {
            backButton.addEventListener('click', goBackToCatalog);
        }
    }
});

// ===== НАВИГАЦИЯ МЕЖДУ КАТАЛОГОМ И ТОВАРОМ =====

// Функция для возврата в каталог с сохранением позиции
function goBackToCatalog(event) {
    if (event) event.preventDefault();

    // Получаем сохраненные данные
    const scrollPosition = sessionStorage.getItem('catalog_scroll') || 0;
    const activeCategory = sessionStorage.getItem('catalog_category') || '';

    // Формируем URL с категорией
    let backUrl = '/';
    if (activeCategory) {
        backUrl = `/?category=${encodeURIComponent(activeCategory)}`;
    }

    // Сохраняем время перехода (для анимации)
    sessionStorage.setItem('last_return_time', Date.now());

    // Переходим на каталог
    window.location.href = backUrl;
}

// Сохраняем позицию и категорию при клике на товар
function saveCatalogState() {
    // Сохраняем позицию скролла
    sessionStorage.setItem('catalog_scroll', window.pageYOffset || document.documentElement.scrollTop);

    // Сохраняем активную категорию из URL
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category') || '';
    sessionStorage.setItem('catalog_category', category);
}

// Простой возврат (запасной вариант)
function simpleGoBack() {
    window.history.back();
    return false;
}

// ===== ИНИЦИАЛИЗАЦИЯ ДЛЯ КАТАЛОГА =====
// Этот код сработает только на странице каталога (/)
if (window.location.pathname === '/') {
    document.addEventListener('DOMContentLoaded', function () {
        // Восстанавливаем позицию при загрузке каталога
        const savedScroll = sessionStorage.getItem('catalog_scroll');
        if (savedScroll) {
            setTimeout(() => {
                window.scrollTo(0, parseInt(savedScroll));
            }, 100);
        }

        // Сохраняем состояние при клике на товар
        document.addEventListener('click', function (e) {
            const productCard = e.target.closest('.product-card.clickable');
            if (productCard) {
                saveCatalogState();
            }
        });
    });
}