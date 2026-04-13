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

try:
    with open ("static/Files/Topology.json" , "r" , encoding="utf-8") as f:
        data = json.load (f)
    tree.cargar_desde_dicc (data)
except:
    print ("No se ha cargado un archivo anterior... Se crea un nuevo arbol")

@app.route("/")
def home():
    """
    Handles the request for the application's home page.
    
    This function invokes the rendering methods for both the generic tree 
    and the BST objects, then provides the resulting graphical data 
    to the 'index.html' template.
    
    Returns:
        Response: The rendered HTML template with embedded graphics.
    """
    grafico_svg = tree.Render ()
    bst_gr = bst.Render ()
    return render_template("index.html", grafico=grafico_svg , bst_grafico = bst_gr)

@app.route ("/Bst/visualization/")
def RenderVisualizationBST():
    """
    API Endpoint that serves the BST visualization as an SVG image.
    
    Instead of returning an HTML page, this route returns the raw SVG 
    data with the correct headers, allowing it to be used as a source 
    for <img> tags or accessed directly via URL.
    
    Returns:
        Response: A Flask response object containing the SVG data 
                  and the 'image/svg+xml' mimetype.
    """
    render = bst.Render ()
    return Response(render, mimetype='image/svg+xml')

@app.route ("/penalization" , methods= ["POST"])
def penalization ():
    """
    Updates the tree penalization limit and records the change for reversion.
    
    This endpoint follows a 'Command' pattern logic where the previous state 
    is backed up before the update is applied.
    
    Payload (JSON):
        { "limit": "number" }
        
    Returns:
        JSON: A success message indicating the limit was updated.
    """
    reversion.Apilar ({"tipo" : "penalization" ,
                       "limit" : tree.getLimit()})
    limit = request.get_json ()
    tree.setLimit (int(limit["limit"]))
    return jsonify ({"message": "ok"})

@app.route ("/ImportarJSON" , methods = ["POST"])                               
def LoadJSON ():
    """
    Parses an uploaded JSON file and populates the system data structures.
    
    The function performs the following:
    1. Validates the presence of the 'archivo' file in the request.
    2. Decodes binary file content to a JSON object.
    3. Populates the main tree and resets the undo stack.
    4. If the data type is 'INSERCION', it populates the BST with flight data.

    Returns:
        JSON: Success or failure message along with the data type processed.
    """
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
    """
    Returns the current state of the flight queue.
    
    This endpoint queries the 'cola_vuelos' object to fetch the total 
    number of pending flights and their respective data.

    Returns:
        JSON: A dictionary containing:
            - 'size' (int): The total number of flights in the queue.
            - 'vuelos' (list): A collection of all flight data objects.
    """
    return jsonify({
        "size":    cola_vuelos.Size(),
        "vuelos":  cola_vuelos.GetAll()
    })
 
@app.route("/Cola/DesencolarVuelo", methods=["POST"])
def Desencolar():
    """
    Transfers a flight from the Queue to the AVL Tree.
    
    This function handles the transition of data between structures, 
    ensuring that every insertion is logged in the reversion stack 
    and that tree penalization rules are updated.

    Returns:
        JSON: 
            - If empty: status 'empty' and a warning message.
            - If success: status 'success', the inserted flight code, 
              and the updated queue list/size.
    """
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
    """
    Registers a new flight into the system queue.
    
    Parses incoming JSON data to create a Flight object and appends it 
    to the global flight queue (cola_vuelos).

    Expected JSON Body:
        {
            "code": "int",
            "origin": "string",
            "destination": "string",
            "departureTime": "string",
            "basePrice": "float",
            "numberPassengers": "int"
        }

    Returns:
        JSON: Success message with status 200 or error details with status 400.
    """
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
    """
    Renders the tree visualization and persists data to the server.
    
    This function performs three main tasks:
    1. Generates an SVG string of the current tree structure.
    2. Serializes the full tree topology to 'Topology.json'.
    3. Serializes the insertion logs to 'Insertion.json'.
    
    Returns:
        Response: An HTTP response containing the SVG image data.
    """
    render = tree.Render ()
    data = tree.SaveTree ()
    with open ("static/Files/Topology.json" , "w" , encoding= "utf-8") as f:
        json.dump (data , f , indent= 4)
    with open ("static/Files/Insertion.json" , "w" , encoding="utf-8") as f:
        json.dump (tree.InsertionSave() , f , indent= 4)
    return Response(render, mimetype='image/svg+xml')

@app.route ("/ModoEstres")
def ModoEstres ():
    """
    Toggles the system's Stress Mode state.
    
    This function switches the 'Stress Mode' in the tree, which likely 
    affects how the tree balances or processes data. The action is 
    stored in the reversion stack to support undo functionality.

    Returns:
        JSON: A message indicating the new state of the Stress Mode:
              - "Modo estres desactivado" (if balance is active)
              - "Modo estres activado" (if balance is inactive)
    """
    reversion.Apilar ({"tipo" : "ModoEstres"})
    tree.SwitchModoEstres ()
    if tree.isBalanceActive ():
        return jsonify ({"message" : "Modo estres desactivado"})
    return jsonify ({"message" : "Modo estres activado"})

@app.route ("/Descargar/Tree")
def SendTree ():
    """
    Saves the current tree state to local JSON files on the server.
    
    This function acts as a manual trigger for data persistence. It writes 
    the current topology and insertion logs to the 'static/Files/' directory 
    using UTF-8 encoding and pretty-print formatting.

    Returns:
        JSON: A simple confirmation message {"message": "ok"} upon 
              successful file writing.
    """
    with open ("static/Files/Topology.json" , "w" , encoding= "utf-8") as f:
        json.dump (tree.SaveTree() , f , indent= 4)
    with open ("static/Files/Insertion.json" , "w" , encoding="utf-8") as f:
        json.dump (tree.InsertionSave() , f , indent= 4)
    return jsonify ({"message" : "ok"})

@app.route ("/Control/Pila")
def ControlZ ():
    """
    Implements the Undo functionality by processing the reversion stack.
    
    This function pops the last action from the 'reversion' stack and 
    applies the corresponding inverse operation to restore the previous 
    state of the tree or application settings.

    Returns:
        JSON: {"message": "ok"} if an action was reverted.
        JSON: {"message": "error"} if the stack is empty.
    """
    if not reversion.isEmpty() :
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
        elif desapila["tipo"] == "EDIT":
            tree.EditFligth (desapila["code"] , desapila["vuelo"])
        tree.depthPenalization ()
        return jsonify ({"message": "ok"})
    return jsonify ({"message" : "error"})

@app.route ("/MassiveCancellation" , methods = ["POST"])
def MassiveCancellation ():
    """
    Performs a bulk removal of flights from the tree structure.
    
    The function identifies a subtree or group based on the provided ID, 
    backups all flights within that group to the reversion stack, 
    and then deletes them from the main tree.

    Payload (JSON):
        { "id": int }

    Returns:
        JSON: A success message {"message": "ok"}.
    """
    id = request.get_json ()["id"]
    reversion.Apilar ({"tipo":"ADD_MULTIPLE", 
                       "vuelos" : tree.TourInsertion(int(id))})
    tree.massiveCancelation (int(id))
    tree.depthPenalization ()

    return jsonify({"message" : "ok"})

@app.route ("/DeleteFligthLessProfitable")
def DeleteFlgith ():
    """
    Finds and removes the least profitable flight from the tree.
    
    The function performs an automated cleanup:
    1. Locates the node with the minimum profit.
    2. Serializes the flight data into a dictionary.
    3. Saves the data to the reversion stack to enable a future 'ADD' undo action.
    4. Removes the node and updates tree penalization metrics.

    Returns:
        JSON: {"message": "ok"} upon successful deletion.
    """
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
    tree.depthPenalization ()
    tree.DeleteFligthLessProfitable ()
    return jsonify ({"message" : "ok"})

@app.route ("/Edit/" , methods = ["POST"])
def EditFligth ():
        """
    Updates an existing flight's details within the tree structure.
    
    The function receives updated parameters via JSON, creates a new 
    Flight instance, and uses the flight code to find and replace 
    the existing record in the AVL or General Tree.

    Payload (JSON):
        {
            "code": int,
            "origin": str,
            "destination": str,
            "departureTime": str,
            "basePrice": float,
            "numberPassengers": int
        }

    Returns:
        JSON: {"message": "ok"} upon successful update.
    """
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
        buscar_vuelo = tree.FindNode (int(data.get("code"))).getFlight()
        reversion.Apilar ({
            "tipo" : "EDIT",
            "code" : int(data.get("code")),
            "vuelo" : buscar_vuelo
        })
        tree.EditFligth (code , nuevo_vuelo)
        tree.depthPenalization()
        return jsonify ({"message" : "ok"})

if __name__ == "__main__":
    app.run(debug=True)