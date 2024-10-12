const tips = [
    "Reduce energy consumption by switching off lights when not needed.",
    "Consider using public transport or walking instead of driving.",
    "Eat more plant-based meals to reduce your carbon footprint.",
    "Unplug electronic devices when not in use to save energy.",
    "Use a reusable water bottle instead of buying plastic ones."
];

function displayRandomTip() {
    const tipElement = document.getElementById('ai-tip');
    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    tipElement.innerText = randomTip;
}

// Actualiza el consejo cada 10 segundos
setInterval(displayRandomTip, 10000);

// Muestra un consejo al cargar la página
window.onload = displayRandomTip;
