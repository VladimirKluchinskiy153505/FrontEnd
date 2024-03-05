 function resetScriptShown() {
        localStorage.removeItem('scriptShown');
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Проверяем, был ли уже показан скрипт для текущего пользователя
        var scriptShown = localStorage.getItem('scriptShown');

        if (!scriptShown) {
            // Запрос даты рождения
            var birthDate = prompt("Введите вашу дату рождения в формате ГГГГ-ММ-ДД:");

            // Парсинг даты и расчет возраста
            var currentDate = new Date();
            var enteredDate = new Date(birthDate);
            var age = currentDate.getFullYear() - enteredDate.getFullYear();

            // Проверка на несовершеннолетних
            if (age < 18) {
                var parentalConsent = confirm("Вы несовершеннолетний. Требуется разрешение родителей для использования сайта. Продолжить?");
                if (!parentalConsent) {
                    alert("Доступ запрещен. Спасибо за понимание.");
                    window.close();
                    // Можно добавить код для перенаправления или других действий при отказе в доступе.
                }
            } else {
                // Вывод возраста
                alert("Ваш возраст: " + age + " лет.");

                // Вывод дня недели для совершеннолетних
                var daysOfWeek = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
                var dayOfWeek = daysOfWeek[enteredDate.getDay()];
                alert("День недели вашего рождения: " + dayOfWeek);

                // Отмечаем, что скрипт был показан пользователю
                localStorage.setItem('scriptShown', 'true');
            }
        }
    });