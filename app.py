from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
cabeza=1
torzo=4
patas=1
busqueda=0

@app.route('/SigCabeza/')
def sigChompa():
    global cabeza
    if cabeza == 4:
        cabeza=1
    else:
        cabeza+=1
    cdx = {}
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("crear.html",cdx=cdx)

@app.route('/SigTorzo/')
def sigTorzo():
    global torzo
    if torzo == 4:
        torzo=1
    else:
        torzo+=1
    cdx = {}
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("crear.html",cdx=cdx)

@app.route('/SigPatas/')
def sigPatas():
    global patas
    if patas == 4:
        patas=1
    else:
        patas+=1
    cdx = {}
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("crear.html",cdx=cdx)

@app.route('/')
def inicio():  # put application's code here
    conexion = sqlite3.connect("db1.db")
    try:
        conexion.execute("""
                            create table avatar(
                            nombre text,
                            cabeza integer,
                            torzo integer,
                            pies integer 
                            )
                        """)
        print("Se creo la tabla avatar")
    except sqlite3.OperationalError:
        print("La tabla avatar ya existe")
    conexion.close()
    cdx = {}
    cdx["busqueda"] = busqueda
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("index.html",cdx=cdx)


@app.route('/crear/')
def crear():  # put application's code here
    cdx = {}
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("crear.html",cdx=cdx)

@app.route('/guardar/', methods=['POST'])
def guardar():
    global busqueda
    conexion = sqlite3.connect("db1.db")
    conexion.execute("insert into avatar(nombre,cabeza,torzo,pies) values (?,?,?,?)", (request.form["name"], cabeza, torzo, patas))
    conexion.commit()
    conexion.close()
    busqueda=0
    cdx = {}
    cdx["busqueda"] = busqueda
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("index.html", cdx=cdx)

@app.route('/buscar/', methods=['POST'])
def buscar():
    global cabeza, torzo, patas, busqueda
    conexion = sqlite3.connect("db1.db")
    cursor = conexion.execute("select * from avatar where nombre="+"'"+request.form["busqueda"]+"'")
    fila = cursor.fetchone()
    cabeza = fila[1]
    torzo = fila[2]
    patas = fila[3]
    busqueda+=1
    cdx = {}
    cdx["busqueda"] = busqueda
    cdx["cabeza"] = cabeza
    cdx["torzo"] = torzo
    cdx["patas"] = patas
    return render_template("index.html", cdx=cdx)

if __name__ == '__main__':
    app.run()
