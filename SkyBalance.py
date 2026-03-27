from Classes.AVL import AVLTree
from Classes.BSTTree import BST
from Classes.FlightSB import Flight
from flask import Flask, jsonify, render_template, request, Response
import json
from Classes.Pila import Pila


app = Flask(__name__)
tree = AVLTree()
reversion = Pila ()

with open ("static/Files/Topology.json" , "r" , encoding="utf-8") as f:
    data = json.load (f)
tree.cargar_desde_dicc (data)

@app.route("/")
def home():
    if tree.root is None:
        print ("el arbol esta vacio")
    grafico_svg = tree.Render ()
    return render_template("index.html", grafico=grafico_svg)

@app.route ("/ImportarJSON" , methods = ["POST"])                               
def LoadJSON ():
    file = request.files.get("archivo")
    if not file:
        print ("Todavia no se ha ingresado un archvivo")
        return jsonify ({"message" : "No cargado"})
    contenido_binario = file.read()
    contenido_texto = contenido_binario.decode("utf-8")
    data = json.loads(contenido_texto)
    tree.cargar_desde_dicc (data)
    print ("Archivo cargado con exito...")
    return jsonify ({"message" : "Exitoso"})




@app.route("/Sent/Node", methods=['POST'])
def RecibirVuelo():
    try:
        data = request.get_json()

        code = int(data.get("code"))
        origin = data.get("origin")
        destination = data.get("destination")
        departureTime = data.get("departureTime")
        basePrice = float(data.get("basePrice"))
        numberPassengers = int(data.get("numberPassengers"))

        nuevo_vuelo = Flight(
            code,
            origin,
            destination,
            departureTime,
            basePrice,
            numberPassengers,
            priority=False,
            promotion=False,
            alert=False
        )

        if type (tree) == BST:
            tree.insertNode (nuevo_vuelo)
        else:
            tree.insertNodeAVL (nuevo_vuelo)

        reversion.Apilar ({
            "tipo" : "REMOVE",
            "codigo" : code
        })


        return jsonify({
            "status": "success",
            "message": f"Vuelo {code} registrado correctamente"
        }), 200


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/Render/Tree", methods=['GET'])
def RenderTreeRoute():
    render = tree.Render ()
    with open ("static/Files/Topology.json" , "w" , encoding= "utf-8") as f:
        json.dump (data , f , indent= 4)
    return Response(render, mimetype='image/svg+xml')

@app.route ("/Descargar/Tree/Topology")
def SendTree ():
    return jsonify ({"Archivo" : tree.SaveTree()})

@app.route ("/Control/Pila")
def ControlZ ():
    if reversion.isEmpty() is False:
        desapila = reversion.Desapilar()
        if desapila ["tipo"] == "REMOVE":
            tree.deleteNode(desapila["codigo"])
        elif desapila ["tipo"] == "ADD":
            v = desapila["vuelo"]

            vuelo = Flight(
                v["code"],
                v["origin"],
                v["destination"],
                v["departureTime"],
                v["basePrice"],
                v["numberPassengers"],
                v["priority"],
                v["promotion"],
                v["alert"]
            tree.insertNodeAVL (vuelo)

if __name__ == "__main__":
    app.run(debug=True)
    data = tree.SaveTree ()
    with open ("static/Files/Topology.json" , "w" , encoding= "utf-8") as f:
        json.dump (data , f , indent= 4)
    print ("Se ha guardado con exito")