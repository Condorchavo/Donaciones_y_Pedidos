// Valida la region
const validadorRegion = (region) => {
  let regiones = regionsInfo["regiones"];

  for (let i=0; i < regiones.length; i++){
    if (region == regiones[i].id){
      return true;
    }
  }
  return false;
}

// Valida la comuna
const validadorComuna = (comuna) => {
  const regionSelection = document.querySelector("#region");

  if (regionSelection.value != ''){
    let comunas = regionsInfo.regiones[regionSelection.value - 1].comunas;
    for (let i=0; i < comunas.length; i++){
      if (comuna == comunas[i].id){
        return true;
      }
    }
  }
  return false;
}

// Valida la direccion
const validadorCalle = (calle) => {
  const calleRGEX = /^([a-zA-Z0-9\s]*)(\s?)(\d{1,})$/;
  return calleRGEX.test(calle);
}

// Valida el tipo de donacion
const validadorTipo = (tipo) => {
  var tipos = ["fruta", "verdura", "otro"]
  return tipo && tipos.includes(tipo);
}

// Valida la cantidad
const validadorCantidad = (cantidad) => cantidad;

// Valida la fecha
const validadorFecha = (fecha) => {
  const dateRGEX = /^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$/;
  const year = fecha.substr(0,4),
        month = fecha.substr(5,2),
        day = fecha.substr(8,2);
  
  const date = new Date();
  const actualYear = date.getFullYear(),
        actualMonth = date.getMonth() + 1,
        actualDay = date.getDate();

  if (fecha && fecha.length == 10 && dateRGEX.test(fecha)){
    if (year > actualYear){
      return true;
    } else if (year == actualYear){
      if (month > actualMonth){
        return true;
      } else if (month == actualMonth && day >= actualDay){
        return true;
      }
    }
  }
  return false;
}

// Valida las fotos
const validadorFoto = (foto1, foto2, foto3, n1, n2, n3) => {
  if (foto1 || foto2 || foto3){
    let typeValid = true;
    const _files = [n1, n2, n3];
    for (let i=0; i<3; i++) {
      // file.type should be "image/<foo>" or "application/pdf"
      const file = document.getElementById(_files[i]);
      if (file.value){
        let fileFamily = file.files[0].type.split("/")[0];
        typeValid &&= fileFamily == "image" || file.files[0].type == "application/pdf";
      }
    }
    return typeValid;
  }
  return false;
}

// Valida el nombre del donante
const validadorNombre = (nombre) => {
  // debe incluir al menos un nombre, y puede incluir tildes y caracteres especiales
  const nombreRGEX = /^([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]*)(\s?)([a-zA-ZñÑáéíóúÁÉÍÓÚ\s]*)$/;
  if (nombreRGEX.test(nombre) && nombre && nombre.length >= 3 && nombre.length<=80) {
    return true;
  }
  return false;
}

// Valida el correo del donante
validadorMail = (mail) => {
  const mailRGEX = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
  return mailRGEX.test(mail);
}

// Valida el número de teléfono del donante (limitado a Chile)
const validadorTelefono = (numero) => {
  if (numero && numero.length <= 15){
    const phoneRGEX = /^(\+?56)?(\s?)\d{1}(\s?)\d{4}(\s?)\d{4}$/;
    return phoneRGEX.test(numero); 
  }
  return true;
}

// Valida todos los campos del formulario
const validarForm = () => {
  let regionInput = document.getElementById("region"),
      comunaInput = document.getElementById("comuna"),
      calleInput = document.getElementById("calle-numero"),
      tipoInput = document.getElementById("tipo"),
      cantidadInput = document.getElementById("cantidad"),
      fechaInput = document.getElementById("fecha-disponibilidad"),
      foto1Input = document.getElementById("foto-1"),
      foto2Input = document.getElementById("foto-2"),
      foto3Input = document.getElementById("foto-3"),
      nombreInput = document.getElementById("nombre"),
      emailInput = document.getElementById("email"),
      celularInput = document.getElementById("celular");

  let regionError = document.getElementById("region-error"),
      comunaError = document.getElementById("comuna-error"),
      calleError = document.getElementById("calle-error"),
      tipoError = document.getElementById("tipo-error"),
      cantidadError = document.getElementById("cantidad-error"),
      fechaError = document.getElementById("fecha-error"),
      fotoError = document.getElementById("foto-error"),
      nombreError = document.getElementById("nombre-error"),
      emailError = document.getElementById("email-error"),
      celularError = document.getElementById("celular-error");

  let msg = '';

  let form = document.getElementById("form_donacion");

  if (!validadorRegion(regionInput.value)){
    msg += 'Seleccione una región válida.\n';
    regionInput.style.borderColor = 'red';
    regionError.style.display="inline";
  } else{
    regionInput.style.borderColor = '';
    regionError.style.display="none";
  }

  if (!validadorComuna(comunaInput.value)){
    msg += 'Elija una comuna!\n';
    comunaInput.style.borderColor = 'red';
    comunaError.style.display="inline";
  } else{
    comunaInput.style.borderColor = '';
    comunaError.style.display="none";
  }
  
  if (!validadorCalle(calleInput.value)){
    msg += 'Primero debe insertar el nombre de la calle y luego el número de la vivienda!\n';
    calleInput.style.borderColor = 'red';
    calleError.style.display="inline";
  } else{
    calleInput.style.borderColor = '';
    calleError.style.display="none";
  }

  if (!validadorTipo(tipoInput.value)){
    msg += 'Elija el tipo de donación!\n';
    tipoInput.style.borderColor = 'red';
    tipoError.style.display="inline";
  } else{
    tipoInput.style.borderColor = '';
    tipoError.style.display="none";
  }

  if (!validadorCantidad(cantidadInput.value)){
    msg += 'Cantidad no válida!\n';
    cantidadInput.style.borderColor = 'red';
    cantidadError.style.display="inline";
  } else{
    cantidadInput.style.borderColor = '';
    cantidadError.style.display="none";
  }

  if (!validadorFecha(fechaInput.value)){
    msg += 'Fecha debe ser mayor o igual a la actual, y su formato debe ser aaaa-mm-dd!\n';
    fechaInput.style.borderColor = 'red';
    fechaError.style.display="inline";
  } else{
    fechaInput.style.borderColor = '';
    fechaError.style.display="none";
  }

  if (!validadorFoto(foto1Input.value, foto2Input.value, foto3Input.value, 'foto-1', 'foto-2', 'foto-3')){
    msg += 'Inserte una foto!\n';
    fotoError.style.display="inline";
  } else{
    fotoError.style.display="none";
  }

  if (!validadorNombre(nombreInput.value)) {
    msg += 'Nombre no válido, debe tener entre 3 y 80 caracteres!\n';
    nombreInput.style.borderColor = 'red';
    nombreError.style.display="inline";
  } else {
    nombreInput.style.borderColor = '';
    nombreError.style.display="none";
  }
  
  if (!validadorMail(emailInput.value)) {
    msg += 'Mail no válido!\n';
    emailInput.style.borderColor = 'red'; // cambiar estilo con JS!!
    emailError.style.display="inline";
  } else {
    emailInput.style.borderColor = '';
    emailError.style.display="none";
  }

  if (!validadorTelefono(celularInput.value)) {
    msg += 'Número celular no válido!\n';
    celularInput.style.borderColor = 'red'; // cambiar estilo con JS!!
    celularError.style.display="inline";
  } else {
    celularInput.style.borderColor = '';
    celularError.style.display="none";
  }

  function Confirm(title, msg, $true, $false, $link, final) { 
    const $content =  "<div class='dialog-ovelay'>" +
                    "<div class='dialog'><header>" +
                     " <h3> " + title + " </h3> " +
                     "<i class='fa fa-close'></i>" +
                 "</header>" +
                 "<div class='dialog-msg'>" +
                     " <p> " + msg + " </p> " +
                 "</div>" +
                 "<footer>" +
                     "<div class='controls'>" +
                         " <button class='button button-danger doAction'>" + $true + "</button> " +
                         " <button class='button button-default cancelAction'>" + $false + "</button> " +
                     "</div>" +
                 "</footer>" +
              "</div>" +
            "</div>";
     $('body').prepend($content);
  if (final){
    $('.doAction').click(function () {
      window.open($link, "_self"); 
      $(this).parents('.dialog-ovelay').fadeOut(500, function () {
        $(this).remove();
      });
    });
  } else {
    $('.doAction').click(function () {
      form.submit();
      $(this).parents('.dialog-ovelay').fadeOut(0, function () {
        $(this).remove();
      });
      Confirm('Confirmación exitosa', 'Hemos recibido la información de su donación. Muchas gracias.', 'Ir al Inicio', 'Volver al formulario', $link, 1);
    });
  }
$('.cancelAction, .fa-close').click(function () {
    $(this).parents('.dialog-ovelay').fadeOut(500, function () {
      $(this).remove();
    });
    return;
  });
}


if (msg == ''){
Confirm('Ventana de Confirmación', '¿Confirma que desea agrega esta donación?', 'Sí, confirmo', 'No, quiero volver al formulario', "../templates/inicio.html");
}
}