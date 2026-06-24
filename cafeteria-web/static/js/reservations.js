document.addEventListener('DOMContentLoaded', function() {
    const resDateInput = document.getElementById('res_date');
    
    if (resDateInput) {
        const today = new Date().toISOString().split('T')[0];
        resDateInput.setAttribute('min', today);
    }

    // Modal de reseñas
    const openBtn = document.getElementById('openReviewModal');
    const closeBtn = document.querySelector('.close-modal');
    const modal = document.getElementById('reviewModal');

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
