document.addEventListener('DOMContentLoaded', () => {
    const cupones = document.querySelectorAll('.cupon');
    const crearCuponFormContainer = document.getElementById('crearCuponFormContainer');
    const toggleFormButton = document.getElementById('toggle-form');

    // Función para obtener colores aleatorios
    function getRandomLightColor() {
        const letters = 'BCDEF'.split('');
        const color1 = '#' + Array.from({ length: 6 }, () => letters[Math.floor(Math.random() * letters.length)]).join('');
        const color2 = '#' + Array.from({ length: 6 }, () => letters[Math.floor(Math.random() * letters.length)]).join('');
        return [color1, color2];
    }

    // Aplicar colores aleatorios a los cupones
    document.querySelectorAll('.cupon-front').forEach(cuponFront => {
        const [color1, color2] = getRandomLightColor();
        cuponFront.style.background = `linear-gradient(45deg, ${color1}, ${color2})`;
    });

    // Función para copiar el código del cupón
    function copyCuponCode(cupon) {
        const cuponCode = cupon.querySelector('.cupon-front h2').textContent;
        navigator.clipboard.writeText(cuponCode).then(() => {
            alert(`Cupón ${cuponCode} copiado al portapapeles!`);
        }).catch(err => {
            console.error('Error al copiar el cupón: ', err);
        });
    }

    // Agregar evento de clic a los cupones
    cupones.forEach(cupon => {
        cupon.addEventListener('click', () => copyCuponCode(cupon));
    });

    // Ocultar el formulario al cargar la página
    crearCuponFormContainer.classList.add('hidden');

    // Evento de clic en el botón para mostrar/ocultar formulario
    toggleFormButton.addEventListener('click', () => {
        crearCuponFormContainer.classList.toggle('hidden');
        toggleFormButton.textContent = crearCuponFormContainer.classList.contains('hidden') ? 'Agregar Cupón' : 'Cancelar';
        toggleFormButton.classList.toggle('cancelar');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const crearCuponForm = document.getElementById('crearCuponForm');
    
    crearCuponForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(crearCuponForm);
        
        try {
            const response = await fetch(crearCuponForm.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: formData,
            });
            
            if (!response.ok) {
                throw new Error("Error al crear el cupón");
            }
            
            const responseData = await response.json();
            console.log("Cupón creado exitosamente:", responseData);
            window.location.reload();
        } catch (error) {
            console.error("Error al crear el cupón:", error);
            // Manejar el error apropiadamente, como mostrar un mensaje al usuario
        }
    });
});

