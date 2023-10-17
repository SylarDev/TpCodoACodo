




function validarFormulario() {
  if (document.contacForm.nombre.value.length <= 2) {
    alert("Ingrese un nombre valido.");
    document.contacForm.nombre.focus();
    return;
  }

  
  let numero = document.contacForm.Telefono.value;

  valor = parseInt(numero);

  // Comprobar si es un valor numérico

  if (isNaN(valor)) {
    alert("Ingrese un numero de telefono valido.");
    document.contacForm.Telefono.focus();
    return;
  }
  document.contacForm.submit();
}
