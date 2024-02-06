const btnsEliminacion  = document.querySelectorAll('.btnEliminacion');

(function () {
    btnsEliminacion.forEach(btn => {
        btn.addEventListener('click', function(e){
            let confirmacion = confirm("¿Confirma la eliminacion del documento ?");
            if(!confirmacion){
                e.preventDefault();
            }
        })
    });
})();