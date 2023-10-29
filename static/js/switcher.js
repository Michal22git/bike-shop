document.addEventListener('DOMContentLoaded', function() {
    var productInfos = document.querySelectorAll('.product-info');
    var currentIndex = 0;

    function showNextProduct() {
        productInfos[currentIndex].style.display = 'none';
        currentIndex = (currentIndex + 1) % productInfos.length;
        productInfos[currentIndex].style.display = 'block';
    }

    productInfos[currentIndex].style.display = 'block';

    setInterval(showNextProduct, 4000);
});