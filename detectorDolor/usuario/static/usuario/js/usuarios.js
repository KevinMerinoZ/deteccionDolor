let debounceTimer = null;

function debounce(func, delay) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(func, delay);
}

function cargarDatos(dato = "", page = 1, tipoDato = "") {
    const url = `/usuarios/buscar-usuarios/?dato=${encodeURIComponent(dato)}&page=${page}&tipoDato=${encodeURIComponent(tipoDato)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('tabla-resultados').innerHTML = data.tabla;
            document.getElementById('paginacion').innerHTML = data.paginacion;
        });
}

if(document.getElementById('filtro')){
document.getElementById('filtro').addEventListener('change', function () {
    const filtro = this.value;

    const inputBuscar = document.getElementById('buscar');
    inputBuscar.focus();
    const dato = inputBuscar.value;
    cargarDatos(dato, 1, filtro);
});
}

// Búsqueda con debounce
if(document.getElementById('buscar')){
    document.getElementById('buscar').addEventListener('keyup', function() {
        const nombre = this.value;
        const filtro = document.getElementById('filtro').value;

        debounce(() => {
            cargarDatos(nombre, 1, filtro);
        }, 300);
    });
}

// Delegación para paginación
document.addEventListener('click', function(e) {
    if(document.getElementById('filtro')){
        const filtro = document.getElementById('filtro').value;
        const enlace = e.target.closest('.link-pagina');

        if(!enlace) return;

        e.preventDefault();
        const page = enlace.dataset.page;
        const nombre = document.getElementById('buscar').value;
        cargarDatos(nombre, page, filtro);
    }
});

// ******** listener general al cargar la página ********
document.addEventListener("DOMContentLoaded", function () {
    // ----- Cargar datos iniciales -----
    if(document.getElementById('filtro')){
        const filtro = document.getElementById('filtro').value;
        cargarDatos("", 1, filtro); // carga la página 1 desde el inicio
    }

    // ----- Manejo de alertas -----
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');

            setTimeout(() => {
                alert.remove();
            }, 1000);
        }, 3000);
    });
});