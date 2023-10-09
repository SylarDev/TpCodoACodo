function actualizarFechaHora() {
    const fechaElement = document.getElementById('fecha');
    const horaElement = document.getElementById('hora');
    
    const fechaActual = new Date();
    const optionsFecha = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const optionsHora = { hour: 'numeric', minute: 'numeric' }; // Configura el formato de la hora deseado

    // Cambia el idioma a español
    const locale = 'es-ES';
    
    fechaElement.textContent = fechaActual.toLocaleDateString(locale, optionsFecha);
    horaElement.textContent = fechaActual.toLocaleTimeString(locale, optionsHora);
}

actualizarFechaHora();

setInterval(function() {
    actualizarFechaHora();
}, 60000); // Actualiza la página cada minuto (60,000 milisegundos)
