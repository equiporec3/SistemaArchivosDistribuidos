import os
import os.path
import datetime
import random
import base64

from pymongo import MongoClient

from Info_archivos import *

def cast_to_info_archivos(documento):
    return Info_archivos(
        archivo=documento['archivo'],
        nombre=documento['nombre'],
        extension=documento['extension'],
        
        fecha_creacion=documento['fecha_creacion'],
        fecha_modificacion=documento['fecha_modificacion'],
        tamano=documento['tamano'],
        ttl=documento['ttl'],

        estado_compartido=documento['estado_compartido'],
        local=documento['local'],
        ip_asociada=documento['ip_asociada'],
        uri_asociada=documento['uri_asociada']
    )

def generar_numero_aleatorio(p_min=0, p_max=100):
    return random.randint(p_min, p_max)
    
def obtener_documentos_en_directorio(ruta_directorio, ip_asociada, uri_asociada):
    try:
        archivos = os.listdir(ruta_directorio)
        lista_documentos = []

        for archivo in archivos:
            ruta_completa = os.path.join(ruta_directorio, archivo)

            if os.path.isfile(ruta_completa):
                

                # info_archivo = Info_archivos(
                #     archivo=str(archivo),
                #     nombre=str(os.path.splitext(archivo)[0]),
                #     extension=str(os.path.splitext(archivo)[1]),

                #     fecha_creacion=str(datetime.datetime.fromtimestamp(os.path.getctime(ruta_completa))),
                #     fecha_modificacion=str(datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa))),
                #     tamano=str(os.path.getsize(ruta_completa)),
                #     ttl=str(generar_numero_aleatorio(50, 100)),
                    
                #     estado_compartido="-",
                #     local=str(True),
                #     ip_asociada="-",
                #     uri_asociada="-"
                # )
                info_archivo = []
                
                info_archivo.append(str(archivo))
                info_archivo.append(str(os.path.splitext(archivo)[0]))
                info_archivo.append(str(os.path.splitext(archivo)[1]))
                info_archivo.append(str(datetime.datetime.fromtimestamp(os.path.getctime(ruta_completa))))
                info_archivo.append(str(datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa))))
                info_archivo.append(str(os.path.getsize(ruta_completa)))
                info_archivo.append(str(generar_numero_aleatorio(50, 100)))
                info_archivo.append("-")
                info_archivo.append(str(True))
                info_archivo.append(str(ip_asociada))
                info_archivo.append(str(uri_asociada))

                lista_documentos.append(info_archivo)

        return lista_documentos
    except FileNotFoundError:
        print(f"El directorio '{ruta_directorio}' no fue encontrado.")
        return []

def borrar_archivo(ubicacion_archivo, nombre_archivo):
    archivo_borrar = ubicacion_archivo + "/" + nombre_archivo
    try:
        os.remove(archivo_borrar)
        print(f"Archivo en {nombre_archivo} eliminado con éxito.")
    except FileNotFoundError:
        print(f"El archivo en {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al intentar eliminar el archivo en {nombre_archivo}: {e}")

def cast_from_list_to_class(lista_de_archivos):
    # Castear a los elementos de la lista a elementos de la clase
    lista_de_elementos = []
    for e in  lista_de_archivos:
        new_e = Info_archivos(
            archivo=e[0],
            nombre=e[1],
            extension=e[2],

            fecha_creacion=e[3],
            fecha_modificacion=e[4],
            tamano=e[5],
            ttl=e[6],
            
            estado_compartido=e[7],
            local=e[8],
            ip_asociada=e[9],
            uri_asociada=e[10]
        )
        lista_de_elementos.append(new_e)
    return lista_de_elementos

# def cast_from_class_to_list(lista_de_archivos):
#     lista_de_elementos = []
#     for e in  lista_de_archivos:
#         for e2 in e:
#             print(e2)
#         print()
#     return lista_de_elementos

def cast_from_document_to_list(documento):
    return [
        documento['archivo'],
        documento['nombre'],
        documento['extension'],
        documento['fecha_creacion'],
        documento['fecha_modificacion'],
        documento['tamano'],
        documento['ttl'],
        documento['estado_compartido'],
        documento['local'],
        documento['ip_asociada'],
        documento['uri_asociada']
    ]


def c_db(lista_de_archivos):
    lista_de_elementos = cast_from_list_to_class(lista_de_archivos)

    # Conexión a la instancia local de MongoDB (por defecto en el puerto 27017)
    client = MongoClient('localhost', 27017)
    # Seleccionar la base de datos 'base_archivos'
    db = client.base_archivos
    # Seleccionar la colección 'coleccion_archivos'
    collection = db.coleccion_archivos

    for info_archivo in lista_de_elementos:
        # Convertir la instancia en un diccionario
        documento = vars(info_archivo)
        # Insertar el documento en la colección
        collection.insert_one(documento)
        # Imprimir el ID asignado al nuevo documento
        # print(f"ID del nuevo documento: {documento['_id']}")
    # print("Elementos insertados.")

def r_db_all():
    # Conexión a la instancia local de MongoDB (por defecto en el puerto 27017)
    client = MongoClient('localhost', 27017)
    # Seleccionar la base de datos 'base_archivos'
    db = client.base_archivos
    # Seleccionar la colección 'coleccion_archivos'
    collection = db.coleccion_archivos

    # Obtener todos los documentos de la colección
    result = collection.find()

    # Imprimir los documentos
    info_archivo_lists = []
    for document in result:
        info_archivo_list = cast_from_document_to_list(document)
        info_archivo_lists.append(info_archivo_list)
        # print(info_archivo_list)
    return info_archivo_lists
    

def r_db_search_all(archivos_buscar):
    # Conexión a la instancia local de MongoDB (por defecto en el puerto 27017)
    client = MongoClient('localhost', 27017)
    # Seleccionar la base de datos 'base_archivos'
    db = client.base_archivos
    # Seleccionar la colección 'coleccion_archivos'
    collection = db.coleccion_archivos

    # Definir el filtro para buscar por el campo 'archivo'
    filtro = {"archivo": archivos_buscar}

    # Obtener los documentos que coinciden con el filtro
    result = collection.find(filtro)

    # Imprimir los documentos 
    info_archivo_lists = []
    for document in result:
        info_archivo_list = cast_from_document_to_list(document)
        info_archivo_lists.append(info_archivo_list)
        # print(info_archivo_list)
    return info_archivo_lists

def r_db_search_one(archivo_buscar):
    # Conexión a la instancia local de MongoDB (por defecto en el puerto 27017)
    client = MongoClient('localhost', 27017)
    # Seleccionar la base de datos 'base_archivos'
    db = client.base_archivos
    # Seleccionar la colección 'coleccion_archivos'
    collection = db.coleccion_archivos

    # Definir el filtro para buscar por el campo 'archivo'
    filtro = {"archivo": archivo_buscar}

    # Obtener el primer documento que coincide con el filtro
    documento_encontrado = collection.find_one(filtro)
    
    info_archivo = cast_from_document_to_list(documento_encontrado)

    # Imprimir el documento encontrado
    # print(info_archivo)
    return info_archivo

def d_db_all():
    client = MongoClient('localhost', 27017)
    db = client.base_archivos
    collection = db.coleccion_archivos
    result = collection.delete_many({})
    print(f"Se han borrado {result.deleted_count} documentos.")

def d_db_filter_many(filename):
    client = MongoClient('localhost', 27017)
    db = client.base_archivos
    collection = db.coleccion_archivos
    result = collection.delete_many({"archivo": filename})
    print(f"Se han borrado {result.deleted_count} documentos con el nombre {filename}.")


def serializar_archivo(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return base64.b64encode(file_content).decode('utf-8')

def deserializar_archivo(file_path, serialized_content):
    # Decodificar la cadena codificada en base64 y guardar en el archivo
    decoded_content = base64.b64decode(serialized_content.encode('utf-8'))
    with open(file_path, 'wb') as file:
        file.write(decoded_content)