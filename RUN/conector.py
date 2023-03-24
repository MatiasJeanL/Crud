from basededatos import obtener_conexion


def insertar_datos(Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO datos(Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo))
    conexion.commit()
    conexion.close()


def obtener_datos():
    conexion = obtener_conexion()
    datos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo FROM datos")
        datos = cursor.fetchall()
    conexion.close()
    return datos


def eliminar_datos(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM datos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_datos_por_id(id):
    conexion = obtener_conexion()
    dato = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo FROM datos WHERE id = %s", (id))
        dato = cursor.fetchone()
    conexion.close()
    return dato


def actualizar_datos(Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE datos SET Nombres=%s, Apellidos=%s, Edad=%s, Lugar=%s, Telefono=%s, direccion=%s,correo=%s WHERE id = %s",
                       (Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo, id))
    conexion.commit()
    conexion.close()