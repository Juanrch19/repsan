document.addEventListener("DOMContentLoaded", function () {
    let openModal = document.getElementById('openModal');
    let modalMapa = document.getElementById('modal');
    let closeBtn = document.getElementById('close');

    // Abrir modal
    openModal.onclick = function () {
        modalMapa.style.visibility = "visible";
    }

    closeBtn.onclick = function () {
        modalMapa.style.visibility = "hidden";
    }

    modalMapa.onclick = function (event) {
        // Verificar si el clic ocurrió dentro del modal-content
        if (event.target.closest('.modal-content')) {
            return; // No hacer nada si el clic ocurrió dentro del contenido del modal
        }

        // Cerrar el modal si el clic ocurrió fuera del modal-content
        modalMapa.style.visibility = "hidden";
    }

    // Redirigir al hacer clic en "Ingresar"
    closeBtn.addEventListener('click', function () {
        window.open("{% url 'cadenavalor' %}", "_blank");
    });
});
