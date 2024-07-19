$(document).ready(function () {
    var authorElements = $('.autor-img');
    $.ajax({
        url: 'https://randomuser.me/api/?results=' + authorElements.length,
        dataType: 'json',
        success: function (data) {
            var autores = data.results;
            authorElements.each(function (index) {
                $(this).attr('src', autores[index].picture.large);
            });
        }
    });

    // Formatear fecha de nacimiento
    $('.fecha-nacimiento .nacimiento').each(function () {
        var fullDate = $(this).text();
        var formattedDate = new Date(fullDate).toISOString().split('T')[0];
        $(this).text(formattedDate);
    });


    // Evento para mostrar/ocultar formulario de crear autor
    $('#toggle-form').on('click', function () {
        if ($('.crear-autor').is(':visible')) {
            $('.crear-autor').hide();
            $('.autores').show();
            $(this).text('Agregar Autor').removeClass('cancelar').css('background-color', '#007bff').hover(function () {
                $(this).css('background-color', '#0056b3');
            }, function () {
                $(this).css('background-color', '#007bff');
            });
        } else {
            $('.autores').hide();
            $('.crear-autor').show();
            $(this).text('Cancelar').addClass('cancelar').css('background-color', 'red').hover(function () {
                $(this).css('background-color', 'darkred');
            }, function () {
                $(this).css('background-color', 'red');
            });
        }
    });
    $('#crearAutorForm').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío por defecto del formulario
    
        var formData = new FormData(this);
        var actionUrl = $(this).attr('action'); // Obtener la URL de acción del formulario
    
        fetch(actionUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: formData,
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Error al crear el autor");
            }
            return response.text(); // Cambiar a response.text() para depurar
        })
        .then((data) => {
            try {
                var jsonData = JSON.parse(data);
                console.log("Autor creado exitosamente:", jsonData);
                
                window.location.href = actionUrl;
            } catch (error) {
                console.error("Error al parsear el JSON:", error);
                console.error("Respuesta recibida:", data);
            }
        })
        .catch((error) => {
            console.error("Error al crear el autor:", error);
        });
    });
});
