(function() {
    var raw = document.getElementById('flash-data').dataset.messages;
    var messages = JSON.parse(raw);  // [ ["categoria", "mensaje"], ... ]

    if (!messages || messages.length === 0) return;

    var container = document.getElementById('toast-container');

    messages.forEach(function(item, index) {
        var category = item[0];  // 'success' o 'error'
        var text     = item[1];

        var icon = category === 'error' ? '✕' : '✓';
        var typeClass = category === 'error' ? 'toast-error' : 'toast-success';

        var toast = document.createElement('div');
        toast.className = 'kaifer-toast ' + typeClass;
        toast.innerHTML =
            '<span class="kaifer-toast__icon">' + icon + '</span>' +
            '<span class="kaifer-toast__body">' + text + '</span>' +
            '<button class="kaifer-toast__close" aria-label="Cerrar">✕</button>';

        container.appendChild(toast);

        // Mostrar con delay escalonado si hay varios
        setTimeout(function() {
            toast.classList.add('show');
        }, index * 150);

        // Cerrar al hacer click en el botón
        toast.querySelector('.kaifer-toast__close').addEventListener('click', function() {
            cerrarToast(toast);
        });

        // Auto-cerrar después de 4 segundos
        setTimeout(function() {
            cerrarToast(toast);
        }, 4000 + index * 150);
    });

    function cerrarToast(toast) {
        toast.classList.remove('show');
        toast.classList.add('hide');
        setTimeout(function() {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 400);
    }
})();