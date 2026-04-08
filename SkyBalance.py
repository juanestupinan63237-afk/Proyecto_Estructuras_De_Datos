from Classes.AVL import AVLTree
from Classes.BinaryTree import BST
from Classes.FlightSB import Flight
from flask import Flask, jsonify, render_template, request, Response
import json
from Classes.Pila import Pila
from Classes.Cola import Cola


app = Flask(__name__)
tree = AVLTree()
bst = BST ()
reversion = Pila ()
cola_vuelos = Cola()

with open ("static/Files/Topology.json" , "r" , encoding="utf-8") as f:
    data = json.load (f)
tree.cargar_desde_dicc (data)

@app.route("/")
def home():
    grafico_svg = tree.Render ()
    bst_gr = bst.Render ()
    return render_template("index.html", grafico=grafico_svg , bst_grafico = bst_gr)

@app.route ("/Bst/visualization/")
def RenderVisualizationBST(dicc: dict):
    render = bst.Render ()
    return Response(render, mimetype='image/svg+xml')

@app.route ("/penalization" , methods= ["POST"])
def penalization ():
    reversion.Apilar ({"tipo" : "penalization" ,
                       "limit" : tree.getLimit()})
    limit = request.get_json ()
    tree.setLimit (int(limit["limit"]))
    return jsonify ({"message": "ok"})

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
    reversion.resetPila()
    if data["tipo"] == "INSERCION":
        bst.cargar_desde_dicc_inserccion (data["vuelos"])
    print ("Archivo cargado con exito...")
    return jsonify ({"message" : "Exitoso" ,
                     "tipo" : data["tipo"]})

@app.route("/Metricas/Analiticas", methods=["GET"])
def MetricasAnaliticas():
    return jsonify(tree.getAnalyticalMetrics())

@app.route("/Cola/Ver", methods=["GET"])
def VerCola():
    return jsonify({
        "size":    cola_vuelos.Size(),
        "vuelos":  cola_vuelos.GetAll()
    })
 
@app.route("/Cola/DesencolarVuelo", methods=["POST"])
def Desencolar():
    vuelo = cola_vuelos.Desencolar()
    if vuelo is None:
        return jsonify({"status": "empty", "message": "La cola está vacía"}), 200

    tree.insertNodeAVL(vuelo)
    reversion.Apilar ({"tipo" : "REMOVE",
                        "codigo" : vuelo.getCode()})
    tree.depthPenalization ()
    return jsonify({
        "status":  "success",
        "message": f"Vuelo {vuelo.getCode()} insertado en el árbol",
        "size":    cola_vuelos.Size(),
        "vuelos":  cola_vuelos.GetAll()
    })

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
        cola_vuelos.Encolar(nuevo_vuelo)
        return jsonify({
            "status": "success",
            "message": f"Vuelo {code} registrado correctamente"
        }), 200


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/Render/Tree", methods=['GET'])
def RenderTreeRoute():
    render = tree.Render ()
    data = tree.SaveTree ()
    with open ("static/Files/Topology.json" , "w" , encoding= "utf-8") as f:
        json.dump (data , f , indent= 4)
    with open ("static/Files/Insertion.json" , "w" , encoding="utf-8") as f:
        json.dump (tree.InsertionSave() , f , indent= 4)
    return Response(render, mimetype='image/svg+xml')

@app.route ("/ModoEstres")
def ModoEstres ():
    reversion.Apilar ({"tipo" : "ModoEstres"})
    tree.SwitchModoEstres ()
    if tree.isBalanceActive ():
        return jsonify ({"message" : "Modo estres desactivado"})
    return jsonify ({"message" : "Modo estres activado"})

@app.route ("/Descargar/Tree")
def SendTree ():
    with open ("static/Files/Topology.json" , "w" , encoding= "utf-8") as f:
        json.dump (tree.SaveTree() , f , indent= 4)
    with open ("static/Files/Insertion.json" , "w" , encoding="utf-8") as f:
        json.dump (tree.InsertionSave() , f , indent= 4)
    return jsonify ({"message" : "ok"})

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
            )
            tree.insertNodeAVL (vuelo)
        elif desapila["tipo"] == "ADD_MULTIPLE":
            vuelos = desapila["vuelos"]
            for i in vuelos:
                tree.insertNodeAVL (i)
        elif desapila["tipo"] == "ModoEstres":
            tree.SwitchModoEstres ()
        elif desapila["tipo"] == "penalization":
            tree.setLimit (desapila["limit"])
        tree.depthPenalization ()
        return jsonify ({"message": "ok"})
    return jsonify ({"message" : "error"})

@app.route ("/MassiveCancellation" , methods = ["POST"])
def MassiveCancellation ():
    id = request.get_json ()["id"]
    reversion.Apilar ({"tipo":"ADD_MULTIPLE", 
                       "vuelos" : tree.TourInsertion(int(id))})
    tree.massiveCancelation (int(id))
    

    return jsonify({"message" : "ok"})

@app.route ("/DeleteFligthLessProfitable")
def DeleteFlgith ():
    node = tree.FindNodeLessProfitable ()
    flight = node.getFlight()
    data = {
        "code" : flight.getCode(),
        "origin" : flight.getOrigin(),
        "destination" : flight.getDestination(),
        "departureTime" : flight.getDepartureTime(),
        "basePrice" : flight.getBasePrice(),
        "numberPassengers" : flight.getNumberPassengers(),
        "priority" : flight.getPriority(),
        "promotion" : flight.getPromotion(),
        "alert" : flight.getAlert ()
        }
    
    reversion.Apilar ({
        "tipo" : "ADD",
        "vuelo" : data
    })
    
    tree.DeleteFligthLessProfitable ()
    return jsonify ({"message" : "ok"})

@app.route ("/Edit/" , methods = ["POST"])
def EditFligth ():
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
        tree.EditFligth (code , nuevo_vuelo)
        tree.depthPenalization()
        return jsonify ({"message" : "ok"})

if __name__ == "__main__":
    app.run(debug=True)