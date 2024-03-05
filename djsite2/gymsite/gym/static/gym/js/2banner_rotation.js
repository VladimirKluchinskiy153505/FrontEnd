document.addEventListener("DOMContentLoaded", function () {
    // Получаем элементы DOM
    const bannerContainers = [
        document.getElementById("banner1-container"),
        document.getElementById("banner2-container")
    ]
    const bannerLinks = [
        document.getElementById("banner1-link"),
        document.getElementById("banner2-link")
    ]
    const bannerImages = [
        document.getElementById("banner1-image"),
        document.getElementById("banner2-image")
    ];
    //const bannerImage = document.getElementById("banner-image");
    const Images = [
        [
            { src: "/static/images/banners/farcry.jpg", link: "https://store.steampowered.com/app/13520/Far_Cry/" },
            { src: "/static/images/banners/assassins.jpg", link: "https://www.ubisoft.com/ru-ru/game/assassins-creed" },
            { src: "/static/images/banners/resident.jpg", link: "https://store.steampowered.com/agecheck/app/1196590/" }
        ],
        [
            {src: "/static/images/banners/vs.jpg", link: "https://visualstudio.microsoft.com/ru/vs/older-downloads/"},
            {src: "/static/images/banners/clion.png", link: "https://www.jetbrains.com/help/clion/installation-guide.html"},
            {src: "/static/images/banners/ws.png", link: "https://www.jetbrains.com/ru-ru/webstorm/"}
        ]
    ];
    // Настройки
    let imageIndex = 0; //текущая показываемая картинка
    let rotationInterval;
    let rotationIntervalTime = document.getElementById("adminInput").value;  // Интервал по умолчанию в миллисекундах
    // Функция для изменения баннера
    function rotateBanner() {
        for(let index=0;index<bannerImages.length;++index) { //Для каждого из двух баннеров
            bannerImages[index].src = Images[index][imageIndex].src;
            bannerLinks[index].href = Images[index][imageIndex].link;

            bannerImages[index].width = 800;
            bannerImages[index].height = 600;
        }
        // Переход к следующему баннеру
        imageIndex  = (imageIndex  + 1) % Images[0].length;
    }
    rotateBanner();
    // Функция для начала ротации
    function startRotation() {
        rotationInterval = setInterval(rotateBanner, rotationIntervalTime);
    }
    // Функция для остановки ротации
    function stopRotation() {
        clearInterval(rotationInterval);
    }
    // Обработчик события при потере фокуса страницы
    window.addEventListener("blur", stopRotation);
    // Обработчик события при восстановлении фокуса страницы
    window.addEventListener("focus", startRotation);
    // Запускаем ротацию
    startRotation();
});