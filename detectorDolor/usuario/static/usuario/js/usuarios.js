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

if(document.getElementById('filtroUsuario')){
document.getElementById('filtroUsuario').addEventListener('change', function () {
    const filtro = this.value;

    const inputBuscar = document.getElementById('buscarUsuario');
    inputBuscar.focus();
    const dato = inputBuscar.value;
    cargarDatos(dato, 1, filtro);
});
}

// Búsqueda con debounce
if(document.getElementById('buscarUsuario')){
    document.getElementById('buscarUsuario').addEventListener('keyup', function() {
        const nombre = this.value;
        const filtro = document.getElementById('filtroUsuario').value;

        debounce(() => {
            cargarDatos(nombre, 1, filtro);
        }, 300);
    });
}

// Delegación para paginación
document.addEventListener('click', function(e) {
    if(document.getElementById('filtroUsuario')){
        const filtro = document.getElementById('filtroUsuario').value;
        const enlace = e.target.closest('.link-pagina');

        if(!enlace) return;

        e.preventDefault();
        const page = enlace.dataset.page;
        const nombre = document.getElementById('buscarUsuario').value;
        cargarDatos(nombre, page, filtro);
    }
});

// ******** listener general al cargar la página ********
document.addEventListener("DOMContentLoaded", function () {
    // ----- Cargar datos iniciales -----
    if(document.getElementById('filtroUsuario')){
        const filtro = document.getElementById('filtroUsuario').value;
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

/* ================================
   lotesAnimales.js
   Gestión dinámica de Lotes de Animales
   ================================ */

// -------------------------
// Función debounce
// -------------------------
function debounce(func, delay) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(func, delay);
}

// -------------------------
// Cargar datos AJAX
// -------------------------
function cargarLotes(dato = "", page = 1, tipoDato = "") {
    const url = `/lotesAnimales/buscar-lotes/?dato=${encodeURIComponent(dato)}&page=${page}&tipoDato=${encodeURIComponent(tipoDato)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tabla = document.getElementById('tabla-lotes');
            const paginacion = document.getElementById('paginacion-lotes');

            if (tabla) tabla.innerHTML = data.tabla;
            if (paginacion) paginacion.innerHTML = data.paginacion;
        })
        .catch(error => console.error("Error en fetch lotes:", error));
}

// ================================
// Filtro: seleccionar tipo de dato
// ================================
const filtroLotes = document.getElementById('filtroLotes');

if (filtroLotes) {
    filtroLotes.addEventListener('change', function () {
        const filtro = this.value;

        const inputBuscar = document.getElementById('buscarLote');
        if (inputBuscar) {
            inputBuscar.focus();
            const dato = inputBuscar.value.trim();
            cargarLotes(dato, 1, filtro);
        }
    });
}

// ================================
// Búsqueda con debounce
// ================================
const inputBuscarLote = document.getElementById('buscarLote');

if (inputBuscarLote) {
    inputBuscarLote.addEventListener('keyup', function () {
        const dato = this.value.trim();
        const filtro = filtroLotes ? filtroLotes.value : "";

        debounce(() => {
            cargarLotes(dato, 1, filtro);
        }, 300);
    });
}

// ================================
// Delegación para paginación
// ================================
document.addEventListener('click', function (e) {
    const filtro = filtroLotes ? filtroLotes.value : null;
    if (filtro === null) return;

    const enlace = e.target.closest('.link-pagina-lotes');
    if (!enlace) return;

    e.preventDefault();

    const page = enlace.dataset.page;
    const dato = inputBuscarLote ? inputBuscarLote.value.trim() : "";

    cargarLotes(dato, page, filtro);
});

// ================================
// Evento general al cargar la página
// ================================
document.addEventListener("DOMContentLoaded", function () {
    console.log("lotesAnimales.js cargado correctamente.");

    // ----- Cargar datos iniciales -----
    if (filtroLotes) {
        const filtro = filtroLotes.value;
        cargarLotes("", 1, filtro);
    }

    // ----- Manejo de alertas -----
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 1000);
        }, 3000);
    });
});