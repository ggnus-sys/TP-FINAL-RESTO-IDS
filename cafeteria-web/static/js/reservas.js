document.addEventListener("DOMContentLoaded", function() {
    const resDateInput = document.getElementById('res_date');
    
    if (resDateInput) {
        const today = new Date().toISOString().split('T')[0];
        resDateInput.setAttribute('min', today);
    }
});