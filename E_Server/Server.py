import Pyro4

from Funciones import *

class Server(object):
    @Pyro4.expose
    def welcomeMessage(self, name):
        return ("Hi welcome " + str (name))

    @Pyro4.expose
    def set_permissions(self):
        info = obtener_documentos_en_directorio(directorio, ip_local, nombre_local)
        return info

    # @Pyro4.expose
    # def get_permissions(self, permisos, info):
    #     print("Permisos recibidos")
    #     for i, e in enumerate(info):
    #         e[7] = permisos[i]
    #     return info

    @Pyro4.expose
    def generar_base_local(self, permisos, info):
        for i, e in enumerate(info):
            e[7] = permisos[i]
        c_db(info)

    @Pyro4.expose
    def leer_base(self):
        resultados = r_db_all()
        # return pickle.dumps(resultados)
        return resultados

    @Pyro4.expose
    def generar_listas(self):
        
        # resultados = r_db_all()
        # ns = Pyro4.locateNS("192.168.100.3")
        # all_names = ns.list()
        # uri = ns.lookup("ARNI")
        # objeto_remoto = Pyro4.Proxy(uri)
        # resultados_ext = objeto_remoto.leer_base()
        # for e in resultados_ext:
        #     e[8] = "Externo"
        # resultados = resultados + resultados_ext
        # return resultados

        
        try:
            resultados = r_db_all()
            ns = Pyro4.locateNS(ip_servidor)
            all_names = ns.list()
            nombres_excluir = ["Pyro.NameServer", nombre_local]
            for name, uri in all_names.items():
                if name not in nombres_excluir:
                    try:
                        objeto_remoto = Pyro4.Proxy(uri)
                        resultados_ext = objeto_remoto.leer_base()
                        for e in resultados_ext:
                            e[8] = "Externo"
                        resultados.extend(resultados_ext)
                    except Exception as e:
                        pass
            return resultados
        except Exception as e:
            print(f"Error al obtener resultados generales: {e}")
            return []

    @Pyro4.expose
    def eliminar_archivo(self, file_name):
        d_db_filter_many(file_name)
        borrar_archivo(directorio, file_name)

    @Pyro4.expose
    def buscar_eliminar_archivo(self, file_name, param_uri):
        if uri == param_uri:
            # borrar localmente
            d_db_filter_many(file_name)
            borrar_archivo(directorio, file_name)
        else:
            # borra externamente
            ns = Pyro4.locateNS(ip_servidor)
            uri_e = ns.lookup(param_uri)
            objeto_remoto = Pyro4.Proxy(uri_e)
            objeto_remoto.eliminar_archivo(file_name)


    @Pyro4.expose
    def copiar_archivo(self, file_name, param_uri):
        ns = Pyro4.locateNS(ip_servidor)
        uri_e = ns.lookup(param_uri)
        objeto_remoto = Pyro4.Proxy(uri_e)
        

        archivo_recibido_serializado = objeto_remoto.generar_archivo(file_name)
        deserializar_archivo(directorio + "/" + file_name, archivo_recibido_serializado)
    
    @Pyro4.expose
    def generar_archivo(self, file_name):
        return serializar_archivo(directorio + "/" + file_name)

def startServer():
    global ip_local
    global ip_servidor
    global uri
    global directorio
    global nombre_local

    ip_local = "192.168.100.4"
    ip_servidor = "192.168.100.3"
    directorio = "C:/Users/GR/Desktop/TEST"
    ruta_archivo="C:/Users/GR/Desktop/Proyect arn/DockerFolder/URI/uri.txt"
    nombre_local = "CHRIS"

    server = Server()
    daemon = Pyro4.Daemon(host=ip_local,port=9095)
    ns = Pyro4.locateNS(ip_servidor)
    uri = daemon.register(server)  
    with open(ruta_archivo, 'w') as file:
        file.write(str(uri))
    ns.register(nombre_local, uri)   
    print(uri)
    daemon.requestLoop() 

if __name__ == "__main__":
    # print(r_db_all())
    # d_db_all()
    # d_db_filter_many("archivo_txt_05.txt")
    startServer()
    pass