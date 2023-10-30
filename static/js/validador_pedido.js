// import { regionsInfo } from './regionesycomunas.js'; 

const validadorRegion = (region) => {
  let regiones = regionsInfo["regiones"];

  for (let i=0; i < regiones.length; i++){
    if (region == regiones[i].id){
      return true;
    }
  }
  return false;
}

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

const validadorTipo = (tipo) => {
  return tipo && (tipo === "fruta" || tipo === "verdura" || tipo === "otro");
}

const validadorDescripcion = (descripcion) => descripcion && descripcion.length <= 250;

const validadorCantidad = (cantidad) => cantidad; // && cantidad.length <= 10

const validadorNombre = (nombre) => {
  let valido = false; 
  if (nombre && nombre.length >= 3 && nombre.length<=80) {
    valido = true;
  }
  return valido
}

const validadorMail = (mail) => {
  var mailRGEX = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
  return mailRGEX.test(mail);
}

const validadorTelefono = (numero) => {
  if (numero && numero.length <= 15){
    var phoneRGEX = /^(\+?56)?(\s?)(0?9)(\s?)\d{4}(\s?)\d{4}$/;
    return phoneRGEX.test(numero);
  }
  return true;
}
const validarForm = () => {
  console.log('Enviando...') // imprimir en consola

  // obtener elementos del DOM por el ID
  let regionInput = document.getElementById('region');
  let comunaInput = document.getElementById('comuna');
  let tipoInput = document.getElementById('tipo');
  let descripcionInput = document.getElementById('descripcion');
  let cantidadInput = document.getElementById('cantidad');
  let nombreInput = document.getElementById('nombre');
  let emailInput = document.getElementById('email');
  let celularInput = document.getElementById('celular');

  let errRegion = document.getElementById('region-error');
  let errComuna = document.getElementById('comuna-error');
  let errTipo = document.getElementById('tipo-error');
  let errDescripcion = document.getElementById('descripcion-error');
  let errCantidad = document.getElementById('cantidad-error');
  let errNombre = document.getElementById('nombre-error');
  let errMail = document.getElementById('email-error');
  let errCelular = document.getElementById('celular-error');
  
  let msg = '';
  
  let form = document.getElementById("form_pedido");

  if (!validadorRegion(regionInput.value)){
    msg += 'Elija una región!\n';
    regionInput.style.borderColor = 'red';
    errRegion.style.display="inline";
  } else{
    regionInput.style.borderColor = '';
    errRegion.style.display="none";
  }

  if (!validadorComuna(comunaInput.value)){
    msg += 'Elija una comuna!\n';
    comunaInput.style.borderColor = 'red';
    errComuna.style.display="inline";
  } else{
    comunaInput.style.borderColor = '';
    errComuna.style.display="none";
  }

  if (!validadorTipo(tipoInput.value)){
    msg += 'Elija el tipo de donación!\n';
    tipoInput.style.borderColor = 'red';
    errTipo.style.display="inline";
  } else{
    tipoInput.style.borderColor = '';
    errTipo.style.display="none";
  }

  if (!validadorDescripcion(descripcionInput.value)){
    msg += 'Descripción no válida!\n';
    descripcionInput.style.borderColor = 'red';
    errDescripcion.style.display="inline";
  } else{
    descripcionInput.style.borderColor = '';
    errDescripcion.style.display="none";
  }

  if (!validadorCantidad(cantidadInput.value)){
    msg += 'Cantidad no válida!\n';
    cantidadInput.style.borderColor = 'red';
    errCantidad.style.display="inline";
  } else{
    cantidadInput.style.borderColor = '';
    errCantidad.style.display="none";
  }

  if (!validadorNombre(nombreInput.value)) {
    msg += 'Nombre malo!\n';
    nombreInput.style.borderColor = 'red';
    errNombre.style.display="inline";
  } else {
    nombreInput.style.borderColor = '';
    errNombre.style.display="none";
  }
  
  if (!validadorMail(emailInput.value)) {
    msg += 'Mail malo!\n';
    emailInput.style.borderColor = 'red';
    errMail.style.display="inline";
  } else {
    emailInput.style.borderColor = '';
    errMail.style.display="none";
  }

  if (!validadorTelefono(celularInput.value)) {
    msg += 'Número celular no válido!\n';
    celularInput.style.borderColor = 'red';
    errCelular.style.display="inline";
  } else {
    celularInput.style.borderColor = '';
    errCelular.style.display="none";
  }


  function Confirm(title, msg, $true, $false, $link, final) {
        var $content =  "<div class='dialog-ovelay'>" +
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
          Confirm('Confirmación exitosa', 'Hemos recibido la información de su pedido. Muchas gracias.', 'Ir al Inicio', 'Volver al formulario', $link, 1);
        });
      }
  $('.cancelAction, .fa-close').click(function () {
        $(this).parents('.dialog-ovelay').fadeOut(500, function () {
          $(this).remove();
        });
      });
   }
  

  if (msg == ''){
    Confirm('Ventana de Confirmación', '¿Confirma que desea agrega este pedido?', 'Sí, confirmo', 'No, quiero volver al formulario', "../templates/inicio.html");
  }
}