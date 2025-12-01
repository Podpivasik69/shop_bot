document.addEventListener('DOMContentLoaded', function () {
    const galleryTrack = document.getElementById('gallery-track');
    const slides = document.querySelectorAll('.slide');
    const currentSlideElement = document.getElementById('current-slide');
    const totalSlidesElement = document.getElementById('total-slides');

    let currentSlide = 0;
    let startX = 0;
    let currentX = 0;
    let isDragging = false;

    totalSlidesElement.textContent = slides.length;

    function updateSlidePosition() {
        galleryTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
        currentSlideElement.textContent = currentSlide + 1;
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

    // Твоя функция drag остается как есть
    function drag(e) {
    if (!isDragging) return;

    e.preventDefault();
    currentX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
    const diff = startX - currentX;

    // Вычисляем смещение
    let offset = (currentSlide * 100) + (diff / window.innerWidth * 100);

    // Резиновый эффект на обеих границах
    if (currentSlide === 0 && offset > 0) {
        // Свайп влево на первой картинке
        offset = offset * 0.3;
    } else if (currentSlide === slides.length - 1 && offset < currentSlide * 100) {
        // Свайп вправо на последней картинке
        offset = currentSlide * 100 + (offset - currentSlide * 100) * 0.3;
    } else if (offset < 0) {
        // Свайп вправо за первую картинку
        offset = offset * 0.3;
    } else if (offset > (slides.length - 1) * 100) {
        // Свайп влево за последнюю картинку
        const overshoot = offset - (slides.length - 1) * 100;
        offset = (slides.length - 1) * 100 + overshoot * 0.3;
    }

    galleryTrack.style.transform = `translateX(-${offset}%)`;
}

    // Инициализация
    updateSlidePosition();
});