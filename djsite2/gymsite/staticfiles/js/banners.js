let banners = ['banner1.jpg', 'banner2.jpg', 'banner3.jpg'];
let bannerIndex = 0;
let rotationInterval;

function rotateBanners() {
    document.getElementById('banner').src = banners[bannerIndex];
    document.getElementById('bannerLink').href = getBannerLink(bannerIndex);
    bannerIndex = (bannerIndex + 1) % banners.length;
}

function startRotation() {
    rotationInterval = setInterval(rotateBanners, 5000);  // Измените интервал по желанию
}

function stopRotation() {
    clearInterval(rotationInterval);
}

function getBannerLink(index) {
    // Вернуть соответствующую ссылку для каждого баннера
    // Например: return '/banner/' + index;
}