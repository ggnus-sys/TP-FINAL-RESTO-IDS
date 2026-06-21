	// Modal de reseñas (aplica en todas las páginas que tengan el modal)
document.addEventListener('DOMContentLoaded', function() {
    var openBtn = document.getElementById('openReviewModal');
    var closeBtn = document.querySelector('.close-modal');
    var modal = document.getElementById('reviewModal');
    if (openBtn && modal) {
        openBtn.addEventListener('click', function() {
            modal.style.display = 'block';
            modal.style.pointerEvents = 'auto';
        });
    }
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            modal.style.pointerEvents = 'none';
        });
    }
});