document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Evitar el comportamiento por defecto del formulario

    // Obtener los datos del formulario
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Crear el objeto de datos
    const datos = {
        email: email,
        password: password
    };

    // Hacer la petición POST al backend
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Redirigir al dashboard si el inicio de sesión fue exitoso
            window.location.href = '/dashboard';  // Redirigir a una página protegida
        } else if (data.error) {
            // Mostrar el mensaje de error en caso de fallo
            document.getElementById('error-message').textContent = data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
