document.addEventListener('DOMContentLoaded', function () {
    var targetTime;
    var countdownInterval;

    // Функция для обновления отображения обратного отсчета
    function updateCountdown() {
        var now = new Date().getTime();
        var distance = targetTime - now;

        // Рассчет часов, минут и секунд
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById('countdown').innerHTML =
            hours + "часов " + minutes + "мин " + seconds + "сек ";

        if (distance <= 0) {
            clearInterval(countdownInterval);
            document.getElementById('countdown').innerHTML = "Время вышло!";
        }
    }
    function resetTimer() {
        clearInterval(countdownInterval);
        targetTime = new Date().getTime() + 3600000; // Установите новое значение времени (1 час в будущем)
        localStorage.setItem('countdownTime', targetTime.toString());
        countdownInterval = setInterval(updateCountdown, 1000);
        updateCountdown(); // Вызывает обновление сразу после сброса
    }

    var savedTime = localStorage.getItem('countdownTime');

    // Если значение сохранено, используем его, иначе устанавливаем отсчет на час
    targetTime = savedTime ? parseInt(savedTime, 10) : new Date().getTime() + 3600000;

    // Обновление отсчета каждую секунду
    countdownInterval = setInterval(updateCountdown, 1000);

    // Добавление обработчиков событий для кнопки "Reset"
    document.getElementById('reset-timer-btn').addEventListener('click', resetTimer);

    // Вызов updateCountdown при загрузке страницы
    updateCountdown();
});