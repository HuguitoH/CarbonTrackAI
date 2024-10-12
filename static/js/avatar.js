document.getElementById('confirm-avatar').addEventListener('click', function() {
    const selectedAvatar = avatars[currentAvatarIndex].name;
    const selectedColor = avatars[currentAvatarIndex].backgroundColor;  // Obtener el color del avatar seleccionado
    const avatarImage = avatars[currentAvatarIndex].animation;  // Ruta de la animación

    // Enviar el avatar, color y la animación al backend
    fetch('/guardar-avatar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            avatar: selectedAvatar, 
            color: selectedColor,  // Enviar el color
            image: avatarImage     // Enviar la animación
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirigir al loader con la información enviada
            window.location.href = `/loader?avatar=${selectedAvatar}&color=${encodeURIComponent(selectedColor)}&image=${encodeURIComponent(avatarImage)}`;
        } else {
            alert('Error al guardar el avatar');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
