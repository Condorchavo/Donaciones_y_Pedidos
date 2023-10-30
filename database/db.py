import json
import os
import pymysql

DB_NAME = "database"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_CHARSET = "utf8"

with open('database/queries.json', 'r') as queries:
    QUERIES = json.load(queries)

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset=DB_CHARSET
    )

# Queries

# Obtiene los datos de la donación a partir de su id
def get_donacion_by_id(id_donacion):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['donacion_por_id'], (id_donacion,))
        return cursor.fetchone()
    
# Obtiene los datos del pedido a partir de su id
def get_pedido_by_id(id_pedido):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['pedido_por_id'], (id_pedido,))
        return cursor.fetchone()
    
# Crea una donación
def crear_donacion(comuna, direccion,
                   tipo, cantidad,
                   fecha, descripcion, condiciones,
                   nombre, email, celular, filenames):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['crear_donacion'], (comuna, direccion,
                                                   tipo, cantidad,
                                                   fecha, descripcion, condiciones,
                                                   nombre, email, celular))
        connection.commit()
        id = cursor.lastrowid
        # for filename in filenames:
        #     cursor.execute(QUERIES['crear_foto_donacion'], (id_donacion, filename))
        # connection.commit()
        return crear_fotos(filenames, id)
    
# Crea un pedido
def crear_pedido(comuna, tipo,
                 cantidad, descripcion,
                 nombre, email, celular):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['crear_pedido'], (comuna, tipo,
                                                  descripcion, cantidad,
                                                  nombre, email, celular))
        connection.commit()
        id = cursor.lastrowid
        return id

# Obtiene los datos de todas las donaciones
def get_donaciones():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['donaciones'],())
        return cursor.fetchall()
    
# Obtiene los datos de todos los pedidos
def get_pedidos():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['pedidos'],())
        return cursor.fetchall()
    
# # Obtiene los datos de todas las donaciones de un usuario
# def get_donaciones_by_user(email):
#     connection = get_connection()
#     with connection.cursor() as cursor:
#         cursor.execute(QUERIES['donaciones_por_usuario'], (email,))
#         return cursor.fetchall()

# # Obtiene los datos de todos los pedidos de un usuario
# def get_pedidos_by_user(email):
#     connection = get_connection()
#     with connection.cursor() as cursor:
#         cursor.execute(QUERIES['pedidos_por_usuario'], (email,))
#         return cursor.fetchall()

# Obtiene las donaciones por página
def donaciones_por_pagina(page):
    val = 5*(page-1)
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['donaciones_por_pagina'], (val,))
        rows = cursor.fetchall()
        remaining = len(rows)
        return rows, remaining
    
# Obtiene los pedidos por página
def pedidos_por_pagina(page):
    val = 5*(page-1)
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['pedidos_por_pagina'], (val,))
        rows = cursor.fetchall()
        remaining = len(rows)
        return rows, remaining
    
# Crea las fotos
def crear_fotos(cosas,id):
    for cosa in cosas:
        connection = get_connection()
        with connection.cursor() as cursor:
            route = os.path.join("uploads", cosa).replace("\\","/")
            cursor.execute(QUERIES["crear_foto"],(route, cosa, id))
            connection.commit()
    return 

# Obtiene las fotos de una donación a partir de su id
def get_fotos_by_id(id_donacion):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['fotos_por_donacion'], (id_donacion,))
        return cursor.fetchall()
    

###############################################
#       Funcionalidades por implementar       #
###############################################
# Elimina las fotos asociadas a una donacion
def delete_fotos_by_id(id_donacion):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(QUERIES['eliminar_fotos_por_donacion'], (id_donacion,))
        connection.commit()

# Elimina una donación a partir de su id
def delete_donacion_by_id(id_donacion):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Elimina las fotos relacionadas
        delete_fotos_by_id(id_donacion)
        cursor.execute(QUERIES['eliminar_donacion'], (id_donacion,))
        connection.commit()
        return cursor.fetchall()
    
# Elimina un pedido a partir de su id
def delete_pedido_by_id(id_pedido):
    connection = get_connection()
    with connection.cursor() as cursor:
        # Elimina las fotos relacionadas
        delete_fotos_by_id(id_pedido)
        connection.commit()
        return cursor.fetchall()