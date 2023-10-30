from database import db
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import cross_origin
from unidecode import unidecode
from utils.validation import *
from werkzeug.utils import secure_filename
import filetype
import hashlib
import unicodedata


UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#############################################
#          Sección: Funciones Auxs          #
#############################################

# Recibe una comuna y retorna su latitud y longitud si es que existe
def get_longitude_latitute(comuna):
    comunas = json.load(open(os.path.join('static', 'js','comunas-Chile.json'), encoding='utf-8'))
    comuna_name = unidecode(unicodedata.normalize('NFKD', comuna).lower())
    for info_comuna in comunas:
        comuna_name_json = unidecode(unicodedata.normalize('NFKD', info_comuna['name']).lower())
        if comuna_name == comuna_name_json:
            return info_comuna['lng'], info_comuna['lat']
    # Si no se encuentra la comuna, se pone en una ubicación por defecto
    lng, lat = "-70.64827", "-33.45694"
    return lng, lat # "not_found", -1 # comuna no encontrada 

# A partir de un id de comuna, retorna el nombre de la región a la que pertenece
def get_region_by_id(comuna_id):
    regiones = json.load(open(os.path.join('static', 'js','region_comuna.json'), "r", encoding='utf-8'))
    for region_info in regiones['regiones']:
        comunas_region = region_info['comunas']
        for comuna in comunas_region:
            if comuna['id'] == comuna_id:
                return region_info['nombre']
            
# A partir de un id de comuna, retorna el nombre de la comuna
def get_comuna_by_id(comuna_id):
    regiones = json.load(open(os.path.join('static', 'js','region_comuna.json'), "r", encoding='utf-8'))
    for region_info in regiones['regiones']:
        comunas_region = region_info['comunas']
        for comuna in comunas_region:
            if comuna['id'] == comuna_id:
                return comuna['nombre']
            
# Retorna una lista con diccionarios asociados
# a las donaciones de la página actual
def donaciones_to_dict():
    donaciones, _ = db.donaciones_por_pagina(1)
    donaciones_list = []
    for donacion in donaciones:
        nombre_comuna = get_comuna_by_id(donacion[1])
        lng, lat = get_longitude_latitute(nombre_comuna)
        donaciones_list.append({
            "id": donacion[0],
            "direccion": donacion[2],
            "tipo": donacion[3],
            "cantidad": donacion[4],
            "fecha": donacion[5].strftime("%Y-%m-%d"),
            "email": donacion[9],
            "lng": lng,
            "lat": lat
        })
    return donaciones_list

# Retorna una lista con diccionarios asociados
# a los pedidos de la página actual
def pedidos_to_dict():
    pedidos, _ = db.pedidos_por_pagina(1)
    pedidos_list = []
    for pedido in pedidos:
        nombre_comuna = get_comuna_by_id(pedido[1])
        lng, lat = get_longitude_latitute(nombre_comuna)
        pedidos_list.append({
            "id": pedido[0],
            "tipo": pedido[2],
            "cantidad": pedido[3],
            "email": pedido[5],
            "lng": lng,
            "lat": lat
        })
    return pedidos_list

# Retorna los filenames de las fotos subidas
def get_filenames(fotos):
    filenames = []
    for foto in fotos:
        if filetype.guess(foto) != None:
            _filename = hashlib.sha256(
                secure_filename(foto.filename).encode('utf-8')).hexdigest()
            _extension = filetype.guess(foto).extension
            img_filename = f'{_filename}.{_extension}'

            # Guarda la imagen en el directorio de uploads
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename).replace("\\","/"))
            filenames.append(img_filename)
    return filenames

##############################################
#        Sección: Validación de Datos        #
##############################################

# Valida que la información de la donación sea correcta
def validar_donacion(region, comuna, direccion,
                     tipo, cantidad, fecha,
                     foto1, foto2, foto3,
                     nombre, email, celular):
    validacion_fotos = validar_fotos([foto1, foto2, foto3])
    errors = [
        validar_region(region),
        validar_comuna(comuna),
        validar_direccion(direccion),
        validar_tipo(tipo),
        validar_cantidad(cantidad),
        validar_fecha(fecha),
        validacion_fotos[0],
        validacion_fotos[1],
        validacion_fotos[2],
        validar_nombre(nombre),
        validar_email(email),
        validar_celular(celular)
    ]
    errors = list(filter(lambda x: x != None, errors))
    return errors

# Valida que la información del pedido sea correcta
def validar_pedido(region, comuna,
                   tipo, cantidad,
                   descripcion,
                   nombre, email, celular):
    errors = [
        validar_region(region),
        validar_comuna(comuna),
        validar_tipo(tipo),
        validar_cantidad(cantidad),
        validar_descripcion(descripcion),
        validar_nombre(nombre),
        validar_email(email),
        validar_celular(celular)
    ]
    errors = list(filter(lambda x: x != None, errors))
    return errors

##############################################
#               Sección: Rutas               #
##############################################

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def redirect_to_home():
    return redirect(url_for('inicio'))

# Ruta de inicio
@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    donaciones = donaciones_to_dict()
    pedidos = pedidos_to_dict()
    return render_template('inicio.html', donaciones=donaciones, pedidos=pedidos)

# Ruta de agregado de donaciones
@app.route('/agregar-donacion', methods=['GET', 'POST'])
def agregar_donacion():
    if request.method == 'POST':
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        direccion = request.form.get('calle-numero')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        fecha = request.form.get('fecha-disponibilidad')
        descripcion = request.form.get('descripcion')
        condiciones = request.form.get('condiciones')
        foto1 = request.files.get('foto-1')
        foto2 = request.files.get('foto-2')
        foto3 = request.files.get('foto-3')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        errors = validar_donacion(region, comuna, direccion,
                                  tipo, cantidad, fecha,
                                  foto1, foto2, foto3,
                                  nombre, email, celular)
        if errors:
            data = {
                "region": region,
                "comuna": comuna,
                "direccion": direccion,
                "tipo": tipo,
                "cantidad": cantidad,
                "fecha": fecha,
                "descripcion": descripcion,
                "condiciones": condiciones,
                "foto1": foto1,
                "foto2": foto2,
                "foto3": foto3,
                "nombre": nombre,
                "email": email,
                "celular": celular
            }
            return render_template('agregar-donacion.html', 
                                   errors=errors,
                                   data=data)
        else:
            filenames = get_filenames([foto1, foto2, foto3])
            db.crear_donacion(str(comuna), direccion, 
                              tipo, cantidad, fecha,
                              descripcion, condiciones,
                              nombre, email, celular,
                              filenames)
            return render_template('agregar-donacion.html')
    if request.method == 'GET':
        return render_template('agregar-donacion.html')
    
# Ruta de agregado de pedidos
@app.route('/agregar-pedido', methods=['GET', 'POST'])
def agregar_pedido():
    if request.method == 'POST':
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        descripcion = request.form.get('descripcion')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        errors = validar_pedido(region, comuna,
                                tipo, cantidad,
                                descripcion,
                                nombre, email, celular)
        if errors:
            data = {
                "region": region,
                "comuna": comuna,
                "tipo": tipo,
                "cantidad": cantidad,
                "descripcion": descripcion,
                "nombre": nombre,
                "email": email,
                "celular": celular
            }
            return render_template('agregar-pedido.html', 
                                   errors=errors,
                                   data=data)
        else:
            db.crear_pedido(str(comuna), tipo, cantidad,
                            descripcion, nombre, email, celular)
            return render_template('agregar-pedido.html')
    if request.method == 'GET':
        return render_template('agregar-pedido.html')
    
# Ruta de visualización de donaciones
@app.route('/ver-donaciones', methods=['GET', 'POST'])
def ver_donaciones():
    page = max(1, int(request.args.get('page', 1)))
    donaciones, remaining = db.donaciones_por_pagina(page)
    data = []
    for donacion in donaciones:
        fotos = db.get_fotos_by_id(donacion[0])
        fotos_list = []
        for i in range(len(fotos)):
            fotos_list.append(url_for('static', filename=f'{fotos[i][0]}'))
        
        _dict = {
            "id": donacion[0],
            "comuna": get_comuna_by_id(donacion[1]),
            "direccion": donacion[2],
            "tipo": donacion[3],
            "cantidad": donacion[4],
            "fecha": donacion[5].strftime("%Y-%m-%d"),
            "descripcion": donacion[6],
            "condiciones": donacion[7],
            "fotos": fotos_list,
            "nombre": donacion[8],
            "email": donacion[9],
            "celular": donacion[10]
        }
        data.append(_dict)
    return render_template('ver-donaciones.html', data=data, page=page, remaining=remaining)

# Ruta de visualización de pedidos
@app.route('/ver-pedidos', methods=['GET', 'POST'])
def ver_pedidos():
    page = max(1, int(request.args.get('page', 1)))
    pedidos, remaining = db.pedidos_por_pagina(page)
    data = []
    for pedido in pedidos:
        _dict = {
            "id": pedido[0],
            "comuna": get_comuna_by_id(pedido[1]),
            "tipo": pedido[2],
            "descripcion": pedido[3],
            "cantidad": pedido[4],
            "nombre": pedido[5],
            "email": pedido[6],
            "celular": pedido[7]
        }
        data.append(_dict)
    return render_template('ver-pedidos.html', data=data, page=page, remaining=remaining)

# Ruta de visualización de gráficos
@app.route('/ver-graficos')
def ver_graficos():
    return render_template('ver-graficos.html')

# Ruta información de la donación
@app.route('/informacion-donacion.html')
def informacion_donacion():
    id_donacion = request.args.get('id')
    donacion = db.get_donacion_by_id(id_donacion)
    fotos = db.get_fotos_by_id(id_donacion)
    fotos_list = []
    for i in range(len(fotos)):
        fotos_list.append(url_for('static', filename=f'{fotos[i][0]}'))
    data = {
        "id": donacion[0],
        "region": get_region_by_id(donacion[1]),
        "comuna": get_comuna_by_id(donacion[1]),
        "comuna_id": donacion[1],
        "direccion": donacion[2],
        "tipo": donacion[3],
        "cantidad": donacion[4],
        "fecha": donacion[5].strftime("%Y-%m-%d"),
        "descripcion": donacion[6],
        "condiciones": donacion[7],
        "fotos": fotos_list,
        "nombre": donacion[8],
        "email": donacion[9],
        "celular": donacion[10]
    }
    return render_template('informacion-donacion.html', 
                           id_donacion=id_donacion, 
                           data=data)

# Ruta información del pedido
@app.route('/informacion-pedido.html')
def informacion_pedido():
    id_pedido = request.args.get('id')
    pedido = db.get_pedido_by_id(id_pedido)
    data = {
        "id": pedido[0],
        "region": get_region_by_id(pedido[1]),
        "comuna": get_comuna_by_id(pedido[1]),
        "comuna_id": pedido[1],
        "tipo": pedido[2],
        "cantidad": pedido[3],
        "descripcion": pedido[4],
        "nombre": pedido[5],
        "email": pedido[6],
        "celular": pedido[7]
    }
    return render_template('informacion-pedido.html', 
                           id_pedido= id_pedido, 
                           data=data)     

# Ruta para obtener los datos de los pedidos
@app.route('/get-donacion-data', methods=['GET'])
@cross_origin(origin='localhost', supports_credentials=True)
def get_donacion_data():
    donaciones = db.get_donaciones()
    donaciones_list = []
    for donacion in donaciones:
        donaciones_list.append(donacion[3])
    return jsonify(donaciones_list)

# Ruta para obtener los datos de los pedidos
@app.route('/get-pedido-data', methods=['GET'])
@cross_origin(origin='localhost', supports_credentials=True)
def get_pedido_data():
    pedidos = db.get_pedidos()
    pedidos_list = []
    for pedido in pedidos:
        pedidos_list.append(pedido[2])
    return jsonify(pedidos_list)   

###############################################
#       Funcionalidades por implementar       #
###############################################

# Ruta de eliminación de donaciones
@app.route('/eliminar-donacion.html', methods=['DELETE'])
def eliminar_donacion():
    if request.method == 'DELETE':
        id_donacion = request.args.get('id')
        db.delete_donacion_by_id(id_donacion)
        return jsonify(link=url_for('ver_donaciones'))  # Redirigir a la página de ver donaciones

# Ruta de eliminación de pedidos
@app.route('/eliminar-pedido.html', methods=['DELETE'])
def eliminar_pedido():
    if request.method == 'DELETE':
        id_pedido = request.args.get('id')
        db.delete_pedido_by_id(id_pedido)
        return jsonify(link=url_for('ver_pedidos'))
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)

