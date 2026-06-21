document.addEventListener('DOMContentLoaded', function () {
    var stars = document.querySelectorAll('.star-rating .star');
    var input = document.getElementById('estrellas');

    if (!stars.length || !input) return;

    stars.forEach(function (star) {
        star.addEventListener('mouseover', function () {
            var val = parseInt(this.dataset.value);
            stars.forEach(function (s) {
                s.style.color = parseInt(s.dataset.value) <= val ? '#c8a96e' : '#ccc';
            });
        });

        star.addEventListener('mouseout', function () {
            var selected = parseInt(input.value) || 0;
            stars.forEach(function (s) {
                s.style.color = parseInt(s.dataset.value) <= selected ? '#c8a96e' : '#ccc';
            });
        });

        star.addEventListener('click', function () {
            input.value = this.dataset.value;
            var selected = parseInt(input.value);
            stars.forEach(function (s) {
                s.style.color = parseInt(s.dataset.value) <= selected ? '#c8a96e' : '#ccc';
            });
        });
    });
});
