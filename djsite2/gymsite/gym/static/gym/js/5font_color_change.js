const styleCheckbox = document.getElementById('styleCheckbox');
    const styleForm = document.getElementById('styleForm');
    const fontSizeInput = document.getElementById('fontSize');
    const textColorInput = document.getElementById('textColor');
    const bgColorInput = document.getElementById('bgColor');
    const resetButton = document.getElementById('reset-color-btn');
    styleCheckbox.addEventListener('change', function() {
        if (styleCheckbox.checked) {
            // Если флажок отмечен, отображаем форму
            styleForm.style.display = 'block';
        } else {
            // Если флажок снят, скрываем форму и сбрасываем стили
            styleForm.style.display = 'none';
            //resetStyles();
        }
    });
    fontSizeInput.addEventListener('input', function() {
        // Изменение размера шрифта
        document.body.style.fontSize = fontSizeInput.value + 'px';
    });
    textColorInput.addEventListener('input', function() {
        // Изменение цвета текста
        document.body.style.color = textColorInput.value;
    });
    bgColorInput.addEventListener('input', function() {
        // Изменение цвета фона
        document.body.style.backgroundColor = bgColorInput.value;
    });
    resetButton.addEventListener('click', function(){
        resetStyles();
    });
    function resetStyles() {
        // Сброс стилей к значениям по умолчанию
        document.body.style.fontSize = '16px';
        document.body.style.color = 'black';
        document.body.style.backgroundColor = '#ffffff';
    }