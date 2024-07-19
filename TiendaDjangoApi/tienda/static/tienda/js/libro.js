function formatFecha(fecha) {
    const date = new Date(fecha);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Obtener todos los elementos con la clase 'fecha-publicacion' y formatear sus fechas
document.querySelectorAll('.fecha-publicacion').forEach(element => {
    element.textContent = formatFecha(element.textContent);
});

document.getElementById('crearLibroForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío automático del formulario

    // Obtener los valores del formulario
    var titulo = document.getElementById('titulo').value;
    var fechaPublicacion = document.getElementById('fechaPublicacion').value;
    var autorLibro = document.getElementById('autorLibro').value;

    // Formatear la fecha a ISO 8601
    fechaPublicacion = new Date(fechaPublicacion).toISOString();

    // Construir el objeto de datos
    var data = {
        titulo: titulo,
        fechaPublicacion: fechaPublicacion,
        autorLibro: autorLibro
    };

    // Realizar la solicitud POST usando Fetch API
    fetch('{% url "crear_libro" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Incluir el token CSRF en el encabezado
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al crear el libro');
        }
        return response.json();
    })
    .then(data => {
        console.log('Libro creado exitosamente:', data);
        // Redirigir a la página de libros u otra acción necesaria
        window.location.href = '{% url "libros" %}';
    })
    .catch(error => {
        console.error('Error al crear el libro:', error);
        // Manejar el error apropiadamente, como mostrar un mensaje al usuario
    });
});

