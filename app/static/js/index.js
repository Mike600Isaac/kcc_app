$(document).ready(function() {
    const dots = $('.pagination-dots .dot');
    let currentIndex = 0;
    const total = dots.length;
    const intervalTime = 5000; // 5 seconds per image

    function showImage(index) {
        // Remove active from all dots
        dots.removeClass('active');
        // Add active to current dot
        dots.eq(index).addClass('active');

        // Get the image from data-img
        let imgUrl = dots.eq(index).data('img');
        $('body').css({
            'background-image': imgUrl,
            'transition': 'background 0.5s ease-in-out'
        });
    }

    // Initial load
    showImage(currentIndex);

    // Auto-scroll every 5s
    let autoScroll = setInterval(function() {
        currentIndex = (currentIndex + 1) % total;
        showImage(currentIndex);
    }, intervalTime);

    // Manual click
    dots.click(function() {
        currentIndex = $(this).index();
        showImage(currentIndex);

        // Reset interval so it doesn't conflict
        clearInterval(autoScroll);
        autoScroll = setInterval(function() {
            currentIndex = (currentIndex + 1) % total;
            showImage(currentIndex);
        }, intervalTime);
    });
});



document.addEventListener("DOMContentLoaded", function () {

    const sliders = document.querySelectorAll(".scroll-row");

    sliders.forEach(slider => {

        // Duplicate cards for infinite loop
        slider.innerHTML += slider.innerHTML;

        let position = 0;
        const speed = 0.4;

        let isPaused = false;

        // Pause when mouse enters
        slider.addEventListener("mouseenter", () => isPaused = true);

        // Resume when mouse leaves
        slider.addEventListener("mouseleave", () => isPaused = false);

        function animate() {

            if (!isPaused) {
                position += speed;   // LEFT → RIGHT movement
            }

            if (position >= slider.scrollWidth / 2) {
                position = 0;
            }

            slider.style.transform = `translateX(${position}px)`;

            requestAnimationFrame(animate);
        }

        animate();
    });

});




