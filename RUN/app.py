from flask import Flask, render_template, request, redirect, session, Response
import mysql.connector
import conector
from flask import make_response
import pdfkit


connection = mysql.connector.connect(host='localhost',
                            user='root',
                            password='palitroche',
                            db='USUARIO_REGISTRO')


cursor = connection.cursor()
app = Flask(__name__)
app.secret_key="super secret key"

@app.route("/")
def index_():
    return render_template('sesion.html')

@app.route("/sesion.html")
def PedirCita():
    return render_template('sesion.html')

@app.route("/index.html")
def index():
    return render_template('index.html', nombre=session['nombre'])

@app.route("/registrar_pacientes.html")
def formulario_agregar_dato():
    return render_template('registrar_pacientes.html')

@app.route("/actualizar.html")
def actualizar():
    return render_template('actualizar.html')

@app.route("/contactanos.html")
def contactanos():
    return render_template('contactanos.html')

@app.route("/quienes_somos.html")
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route("/servicios.html")
def servicios():
    return render_template('servicios.html')

@app.route("/pedir_cita.html")
def pedir_cita():
    return render_template('pedir_cita.html')

@app.route("/registrarse.html")
def registrarse():
    return render_template('registrarse.html')

@app.route("/pre_pdf.html")
def pre_pdf():
    return render_template('pre_pdf.html')

@app.route("/imprimir_pdf.html")
def imprimir_pdf():
    return render_template('pdf.html')

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    contraseña = request.form["contraseña"]
    correo = request.form["correo"]
    start = f"INSERT INTO DATA(nombre, apellido, telefono, contraseña, correo) VALUES ('{nombre}', '{apellido}', '{telefono}', '{contraseña}', '{correo}')"
    cursor.execute(start)
    connection.commit()

    return redirect("/sesion.html")

@app.route("/logueo", methods=['GET', 'POST'])
def logueo():
    msg=''
    if request.method=='POST':
        nombre =request.form['nombre']
        contraseña = request.form["contraseña"]
        cursor.execute("SELECT nombre, contraseña FROM DATA WHERE nombre=%s AND contraseña=%s",(nombre, contraseña))
        record = cursor.fetchone()
        if record:
            session['logeado']=True
            session['nombre']= record[0]
            return redirect("/index.html")
        else:
            msg='no se encontró el usuario'
    return render_template('sesion.html')

@app.route('/salir')
def salir():
    session.pop('logeado', None)
    session.pop('nombre', None)

    return redirect("/sesion.html")


@app.route("/guardar_paciente", methods=["POST"])
def guardar_paciente():
    Nombres = request.form["Nombres"]
    Apellidos = request.form["Apellidos"]
    Edad = request.form["Edad"]
    Lugar = request.form["Lugar"]
    Telefono = request.form["Telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    conector.insertar_datos(Nombres, Apellidos, Edad,Lugar, direccion, Telefono, correo)

    return redirect("/datos")


@app.route("/datos")
def datos():
    datos = conector.obtener_datos()
    return render_template("datos.html", datos=datos)


@app.route("/eliminar_juego", methods=["POST"])
def eliminar_datos():
    conector.eliminar_datos(request.form["id"])
    return redirect("/datos")


@app.route("/editar_dato/<int:id>")
def editar_dato(id):
    dato = conector.obtener_datos_por_id(id)
    return render_template("actualizar.html", dato=dato)

@app.route("/pdf/<int:id>")
def pdf(id):
    dato = conector.obtener_datos_por_id(id)
    return render_template("pre_pdf.html", dato=dato)


@app.route("/actualizar_dato", methods=["POST"])
def actualizar_dato():
    id = request.form["id"]
    Nombres = request.form["Nombres"]
    Apellidos = request.form["Apellidos"]
    Edad = request.form["Edad"]
    Lugar = request.form["Lugar"]
    Telefono = request.form["Telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    conector.actualizar_datos(Nombres, Apellidos, Edad, Lugar, Telefono, direccion, correo, id)

    return redirect("/datos")

@app.route('/pdf', methods =["POST"])
def pdf_imprimir():
    id = request.form["id"]
    Nombres = request.form["Nombres"]
    Apellidos = request.form["Apellidos"]
    Edad = request.form["Edad"]
    Lugar = request.form["Lugar"]
    Telefono = request.form["Telefono"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    conector.actualizar_datos(Nombres, Apellidos, Edad,Lugar, direccion, Telefono, correo, id)
    html = render_template("impresion_pdf.html", Nombres=Nombres, Apellidos=Apellidos, Edad= Edad, Lugar=Lugar, Telefono=Telefono, direccion= direccion, correo=correo)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response
    return render_template("pdf_pdf.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=4000)