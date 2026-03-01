from Classes.AVL import AVLTree
from Classes.FlightSB import Flight
from flask import Flask, jsonify, render_template, request, Response

# Inicialización de la App y el Árbol
app = Flask(__name__)
tree = AVLTree()

@app.route("/")
def home():
    """
    Ruta principal que carga la interfaz.
    Envía el primer renderizado del árbol (vacío o con datos iniciales).
    """
    grafico_svg = tree.RenderTree()
    return render_template("index.html", grafico=grafico_svg)

@app.route("/Sent/Node", methods=['POST'])
def RecibirVuelo():
    """
    Recibe los datos del formulario en formato JSON,
    crea el objeto Flight e inserta el nodo en el AVL.
    """
    try:
        data = request.get_json()

        # Conversión de tipos para asegurar que la lógica del AVL no falle
        code = int(data.get("code"))
        origin = data.get("origin")
        destination = data.get("destination")
        departureTime = data.get("departureTime")
        basePrice = float(data.get("basePrice"))
        numberPassengers = int(data.get("numberPassengers"))

        # Crear el objeto de vuelo
        nuevo_vuelo = Flight(
            code, origin, destination, departureTime,
            basePrice, numberPassengers,
            priority=False, promotion=False, alert=False
        )

        # Insertar en el árbol
        tree.insertNode(nuevo_vuelo)

        return jsonify({
            "status": "success", "message": f"Vuelo {code} registrado correctamente"
        }), 200

    except Exception as e:
        print(f"Error detectado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/Render/Tree", methods=['GET'])
def RenderTreeRoute():
    """
    Ruta que devuelve únicamente el código SVG del árbol.
    Es llamada por el JavaScript (app.js) para actualizar la imagen.
    """
    svg = tree.RenderTree()
    return Response(svg, mimetype='image/svg+xml')

@app.route("/Print", methods=['POST'])
def PrintPreOrder():
    """
    Devuelve el recorrido PreOrder en formato JSON para mostrarlo en una alerta.
    """
    result = tree.preorderTour()
    return jsonify({"preorder": result})

if __name__ == "__main__":
    # Ejecuta el servidor en modo debug para ver cambios en tiempo real
    app.run(debug=True, port=5000)