document.addEventListener("DOMContentLoaded", function() {
    const resDateInput = document.getElementById('res_date');
    
    // Verificamos que el elemento exista en la página antes de actuar
    if (resDateInput) {
        const today = new Date().toISOString().split('T')[0];
        resDateInput.setAttribute('min', today);
    }
});