document.addEventListener('DOMContentLoaded', () => {
    // Para cambiar el progreso de los círculos
    const circles = document.querySelectorAll('.outer-circle');

    circles.forEach(circle => {
        const progress = circle.getAttribute('data-progress');
        const degree = progress * 360;
        circle.style.setProperty('--progress', `${degree}deg`);
    });

    // Cambios de tips de IA
    const tips = [
        "Consider using public transport or walking instead of driving.",
        "Turn off unnecessary lights when not in use.",
        "Reduce water consumption by taking shorter showers."
    ];

    let currentTipIndex = 0;
    const aiTips = document.querySelector('.tip-text');

    setInterval(() => {
        currentTipIndex = (currentTipIndex + 1) % tips.length;
        aiTips.textContent = tips[currentTipIndex];
    }, 10000);
});



var avatarAnimation = lottie.loadAnimation({
    container: document.getElementById('avatar-animation'), // Contenedor donde se mostrará la animación
    renderer: 'svg', // Puede ser 'canvas' o 'svg'
    loop: true, // Si deseas que la animación se repita
    autoplay: true, // Reproducir automáticamente al cargar
    path: "{{ url_for('static', filename=usuario.avatar) }}" 
});
