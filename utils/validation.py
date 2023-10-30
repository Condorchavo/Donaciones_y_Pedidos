import datetime
import filetype
import json
import os
import re

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_MIMETYPES = {'image/png', 'image/jpeg', 'image/gif', 'image/jpg'}

# Valida la región
def validar_region(region):
    regiones = os.path.join("static", "js", "region_comuna.json")
    with open(regiones, "r") as regions_file:
        regions_info = json.load(regions_file)
        regiones = regions_info["regiones"]
        for region_info in regiones:
            if region == str(region_info["id"]):
                return None
        return "Región no válida!"

# Valida la comuna
def validar_comuna(comuna):
    regiones = os.path.join("static", "js", "region_comuna.json")
    with open(regiones, "r") as regions_file:
        regions_info = json.load(regions_file)
        regiones = regions_info["regiones"]
        for region_info in regiones:
            comunas = region_info["comunas"]
            for comuna_info in comunas:
                if comuna == str(comuna_info["id"]):
                    return None
    return "Comuna no válida!"

# Valida la dirección
def validar_direccion(direccion):
    calle_regex = r"^([a-zA-Z0-9\s]*)(\s?)(\d{1,})$"
    if bool(re.match(calle_regex, direccion)) and len(direccion) <= 80:
        return None
    return "Primero debe insertar el nombre de la calle y luego el número de la vivienda!"

# Valida el tipo de donación
def validar_tipo(tipo):
    tipos_validos = ["fruta", "verdura", "otro"]
    if tipo and tipo in tipos_validos:
        return None
    return "Elija el tipo de donación!"

# Valida la descripción
def validar_descripcion(descripcion):
    if descripcion and len(descripcion) <= 250:
        return None
    return 'Descripción no válida!'

# Valida la cantidad
def validar_cantidad(cantidad):
    if bool(cantidad) and len(cantidad) <= 10:
        return None
    return 'Primero debe insertar el nombre de la calle y luego el número de la vivienda!'

# Valida la fecha
def validar_fecha(fecha):
    date_rgex = r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"
    year = int(fecha[:4])
    month = int(fecha[5:7])
    day = int(fecha[8:10])

    if fecha and len(fecha) == 10 and re.match(date_rgex, fecha):
        current_date = datetime.datetime.now().date()
        actualYear = current_date.year
        actualMonth = current_date.month
        actualDay = current_date.day
        if year > actualYear:
            return None
        elif year == actualYear:
            if month > actualMonth:
                return None
            elif month == actualMonth and day >= actualDay:
                    return None
    return "Fecha debe ser mayor o igual a la actual, y su formato debe ser aaaa-mm-dd!"

# Valida las fotos
def validar_fotos(fotos):
    mensajes = []
    for foto in fotos:
        if foto is None:
            mensajes.append("Inserte una foto!")
            continue
        if foto.filename == '':
            mensajes.append("Imagen es un archivo vacío!")
            continue
        ftype_guess = filetype.guess(foto)
        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            mensajes.append("Extensión de la imagen no válida! Debe ser .png, .jpg, .jpeg o .gif")
            continue
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            mensajes.append("MIME no válido!")
            continue
        mensajes.append("Imagen insertada correctamente!")
    mensajes2 = [None] * len(fotos)
    if all(elem == "Inserte una foto!" for elem in mensajes):
        mensajes2[0] = "No se insertaron fotos!"
    elif "Imagen insertada correctamente" in mensajes:
        mensajes2[0] = "Imagen insertada correctamente!"
    else:
        for i in range(len(fotos)):
            if mensajes[i] != None:
                mensajes2.append("Imagen "+str(i+1)+": "+mensajes[i])
    return mensajes2

# Valida el nombre
def validar_nombre(nombre):
    if nombre and 3 <= len(nombre) <= 80:
        return None
    return 'El nombre es requerido y debe tener entre 3 y 80 caracteres!'

# Valida el email
def validar_email(email):
    mail_regex = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x7f])+)\])"
    if bool(re.match(mail_regex, email)) and len(email) <= 30:
        return None
    return "Mail no válido!"

# Valida el celular
def validar_celular(numero):
    if numero and len(numero) <= 15:
        phone_regex = r"^(\+?56)?(\s?)\d{1}(\s?)\d{4}(\s?)\d{4}$"
        if bool(re.match(phone_regex, numero)):
            return None
        else:
            return 'Número celular no válido!'
    return None