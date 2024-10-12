document.getElementById('registroForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el comportamiento por defecto del formulario

    // Obtener los datos del formulario
    const nombre = document.getElementById('first_name').value;
    const apellido = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Crear un objeto con los datos del formulario
    const datos = {
        nombre: `${nombre} ${apellido}`,
        email: email,
        avatar: 'default-avatar',  // Puedes reemplazar esto con el avatar que el usuario seleccione
        password: password  // Asegúrate de que la contraseña se envía correctamente
    };

    // Enviar los datos al backend usando fetch
        // Enviar los datos al backend usando fetch
    fetch('/registro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
        })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
        // Redirigir a la página de selección de avatar si el registro es exitoso
            window.location.href = '/seleccion-avatar';
        } else if (data.error) {
            alert(data.error);
         }
        })
    .catch(error => {
    console.error('Error:', error);
    });
});

