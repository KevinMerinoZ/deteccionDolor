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

    const enlace = e.target.closest('.link-pagina');
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

/* ================================
   provedor.js
   Gestión dinámica de Proveedores
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
function cargarProveedores(dato = "", page = 1, tipoDato = "") {

    const url = `/provedor/buscar-proveedor/?dato=${encodeURIComponent(dato)}&page=${page}&tipoDato=${encodeURIComponent(tipoDato)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tabla = document.getElementById('tabla-proveedores');
            const paginacion = document.getElementById('paginacion-proveedores');

            if (tabla) tabla.innerHTML = data.tabla;
            if (paginacion) paginacion.innerHTML = data.paginacion;
        })
        .catch(error => console.error("Error en fetch proveedores:", error));
}

// ================================
// Filtro: seleccionar tipo de dato
// ================================
const filtroProveedores = document.getElementById('filtroProveedor');

if (filtroProveedores) {
    filtroProveedores.addEventListener('change', function () {
        const filtro = this.value;

        const inputBuscar = document.getElementById('buscarProveedor');
        if (inputBuscar) {
            inputBuscar.focus();
            const dato = inputBuscar.value.trim();
            cargarProveedores(dato, 1, filtro);
        }
    });
}

// ================================
// Búsqueda con debounce
// ================================
const inputBuscarProveedor = document.getElementById('buscarProveedor');

if (inputBuscarProveedor) {
    inputBuscarProveedor.addEventListener('keyup', function () {
        const dato = this.value.trim();
        const filtro = filtroProveedores ? filtroProveedores.value : "";

        debounce(() => {
            cargarProveedores(dato, 1, filtro);
        }, 300);
    });
}

// ================================
// Delegación para paginación
// ================================
document.addEventListener('click', function (e) {
    const filtro = filtroProveedores ? filtroProveedores.value : null;
    if (filtro === null) return;

    const enlace = e.target.closest('.link-pagina');

    if (!enlace) return;

    e.preventDefault();

    const page = enlace.dataset.page;
    const dato = inputBuscarProveedor ? inputBuscarProveedor.value.trim() : "";

    if (!page) return;

    cargarProveedores(dato, page, filtro);
});

// ================================
// Evento general al cargar la página
// ================================
document.addEventListener("DOMContentLoaded", function () {
    console.log("provedor.js cargado correctamente.");

    // Cargar datos iniciales
    if (filtroProveedores) {
        const filtro = filtroProveedores.value;
        cargarProveedores("", 1, filtro);
    }

    // Manejo de alertas desaparecidas
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 1000);
        }, 3000);
    });
});

/* ================================
   farmaco.js
   Gestión dinámica de Fármacos
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
function cargarFarmacos(dato = "", page = 1, tipoDato = "") {

    const url = `/farmaco/buscar-farmaco/?dato=${encodeURIComponent(dato)}&page=${page}&tipoDato=${encodeURIComponent(tipoDato)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tabla = document.getElementById('tabla-farmacos');
            const paginacion = document.getElementById('paginacion-farmacos');

            if (tabla) tabla.innerHTML = data.tabla;
            if (paginacion) paginacion.innerHTML = data.paginacion;
        })
        .catch(error => console.error("Error en fetch farmacos:", error));
}

// ================================
// Filtro: seleccionar tipo de dato
// ================================
const filtroFarmacos = document.getElementById('filtroFarmaco');

if (filtroFarmacos) {
    filtroFarmacos.addEventListener('change', function () {
        const filtro = this.value;

        const inputBuscar = document.getElementById('buscarFarmaco');
        if (inputBuscar) {
            inputBuscar.focus();
            const dato = inputBuscar.value.trim();
            cargarFarmacos(dato, 1, filtro);
        }
    });
}

// ================================
// Búsqueda con debounce
// ================================
const inputBuscarFarmaco = document.getElementById('buscarFarmaco');

if (inputBuscarFarmaco) {
    inputBuscarFarmaco.addEventListener('keyup', function () {
        const dato = this.value.trim();
        const filtro = filtroFarmacos ? filtroFarmacos.value : "";

        debounce(() => {
            cargarFarmacos(dato, 1, filtro);
        }, 300);
    });
}

// ================================
// Delegación para paginación
// ================================
document.addEventListener('click', function (e) {
    const filtro = filtroFarmacos ? filtroFarmacos.value : null;
    if (filtro === null) return;

    const enlace = e.target.closest('.link-pagina');

    if (!enlace) return;

    e.preventDefault();

    const page = enlace.dataset.page;
    const dato = inputBuscarFarmaco ? inputBuscarFarmaco.value.trim() : "";

    if (!page) return;

    cargarFarmacos(dato, page, filtro);
});

// ================================
// Evento general al cargar la página
// ================================
document.addEventListener("DOMContentLoaded", function () {
    console.log("farmaco.js cargado correctamente.");

    // Cargar datos iniciales
    if (filtroFarmacos) {
        const filtro = filtroFarmacos.value;
        cargarFarmacos("", 1, filtro);
    }

    // Manejo de alertas desaparecidas
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 1000);
        }, 3000);
    });
});

/* ================================
   material.js
   Gestión dinámica de Materiales
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
function cargarMateriales(dato = "", page = 1, tipoDato = "") {

    const url = `/material/buscar-material/?dato=${encodeURIComponent(dato)}&page=${page}&tipoDato=${encodeURIComponent(tipoDato)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tabla = document.getElementById('tabla-materiales');
            const paginacion = document.getElementById('paginacion-materiales');

            if (tabla) tabla.innerHTML = data.tabla;
            if (paginacion) paginacion.innerHTML = data.paginacion;
        })
        .catch(error => console.error("Error en fetch materiales:", error));
}

// ================================
// Filtro: seleccionar tipo de dato
// ================================
const filtroMaterial = document.getElementById('filtroMaterial');

if (filtroMaterial) {
    filtroMaterial.addEventListener('change', function () {
        const filtro = this.value;

        const inputBuscar = document.getElementById('buscarMaterial');
        if (inputBuscar) {
            inputBuscar.focus();
            const dato = inputBuscar.value.trim();
            cargarMateriales(dato, 1, filtro);
        }
    });
}

// ================================
// Búsqueda con debounce
// ================================
const inputBuscarMaterial = document.getElementById('buscarMaterial');

if (inputBuscarMaterial) {
    inputBuscarMaterial.addEventListener('keyup', function () {
        const dato = this.value.trim();
        const filtro = filtroMaterial ? filtroMaterial.value : "";

        debounce(() => {
            cargarMateriales(dato, 1, filtro);
        }, 300);
    });
}

// ================================
// Delegación para paginación
// ================================
document.addEventListener('click', function (e) {

    const filtro = filtroMaterial ? filtroMaterial.value : null;
    if (filtro === null) return;

    const enlace = e.target.closest('.link-pagina');
    if (!enlace) return;

    e.preventDefault();

    const page = enlace.dataset.page;
    const dato = inputBuscarMaterial ? inputBuscarMaterial.value.trim() : "";

    if (!page) return;

    cargarMateriales(dato, page, filtro);
});

// ================================
// Evento general al cargar la página
// ================================
document.addEventListener("DOMContentLoaded", function () {
    console.log("material.js cargado correctamente.");

    // Cargar datos iniciales
    if (filtroMaterial) {
        const filtro = filtroMaterial.value;
        cargarMateriales("", 1, filtro);
    }

    // Manejo de alertas desaparecidas
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 1000);
        }, 3000);
    });
});

/* ==========================================
   sustanciaExperimental.js
   Gestión dinámica de Sustancias Experimentales
   ========================================== */

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
function cargarSustancias(dato = "", page = 1, tipoDato = "") {

    const url = `/sustanciasExperimentales/buscar-sustancia/?dato=${encodeURIComponent(dato)}&page=${page}&tipoDato=${encodeURIComponent(tipoDato)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tabla = document.getElementById('tabla-sustancias');
            const paginacion = document.getElementById('paginacion-sustancias');

            if (tabla) tabla.innerHTML = data.tabla;
            if (paginacion) paginacion.innerHTML = data.paginacion;
        })
        .catch(error => console.error("Error en fetch sustancias:", error));
}

// ================================
// Filtro: seleccionar tipo de dato
// ================================
const filtroSustancias = document.getElementById('filtroSustancia');

if (filtroSustancias) {
    filtroSustancias.addEventListener('change', function () {
        const filtro = this.value;

        const inputBuscar = document.getElementById('buscarSustancia');
        if (inputBuscar) {
            inputBuscar.focus();
            const dato = inputBuscar.value.trim();
            cargarSustancias(dato, 1, filtro);
        }
    });
}

// ================================
// Búsqueda con debounce
// ================================
const inputBuscarSustancia = document.getElementById('buscarSustancia');

if (inputBuscarSustancia) {
    inputBuscarSustancia.addEventListener('keyup', function () {
        const dato = this.value.trim();
        const filtro = filtroSustancias ? filtroSustancias.value : "";

        debounce(() => {
            cargarSustancias(dato, 1, filtro);
        }, 300);
    });
}

// ================================
// Delegación para paginación
// ================================
document.addEventListener('click', function (e) {
    const filtro = filtroSustancias ? filtroSustancias.value : null;
    if (filtro === null) return;

    const enlace = e.target.closest('.link-pagina');
    if (!enlace) return;

    e.preventDefault();

    const page = enlace.dataset.page;
    const dato = inputBuscarSustancia ? inputBuscarSustancia.value.trim() : "";

    if (!page) return;

    cargarSustancias(dato, page, filtro);
});

// ================================
// Evento general al cargar la página
// ================================
document.addEventListener("DOMContentLoaded", function () {
    console.log("sustanciaExperimental.js cargado correctamente.");

    // Cargar datos iniciales
    if (filtroSustancias) {
        const filtro = filtroSustancias.value;
        cargarSustancias("", 1, filtro);
    }

    // Manejo de alertas desaparecidas
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 1000);
        }, 3000);
    });
});
