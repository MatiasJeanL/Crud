import pymysql


def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='palitroche',
                                db='AGREGAR_PACIENTES')