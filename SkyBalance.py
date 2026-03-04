from flask import Flask, render_template, request, jsonify, Response
from Classes.AVL import AVLTree
from Classes.FlightSB import Flight
import json

app = Flask(__name__)

tree = AVLTree()
with open ("Files/Topology.json" , "r" , encoding = "utf-8") as f:
    data = json.load (f)
tree.cargar_desde_dicc (data)

# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    return render_template("index.html")


# ===============================
# INSERTAR NODO
# ===============================
@app.route("/Sent/Node", methods=["POST"])
def insert_node():
    data = request.json

    try:
        # Crear objeto Flight correctamente
        flight = Flight(
            int(data["code"]),
            data["origin"],
            data["destination"],
            data["departureTime"],
            float(data["basePrice"]),
            int(data["numberPassengers"])
        )

        # Insertar en AVL
        tree.insertNodeAVL(flight)

        return jsonify({"message": "Vuelo insertado correctamente"})

    except Exception as e:
        print("ERROR INSERT:", e)
        return jsonify({"message": str(e)}), 400


# ===============================
# RENDER AVL
# ===============================
@app.route("/Render/AVL", methods=["GET"])
def render_tree():
    print("ROOT ACTUAL:", tree.root)  # Debug temporal
    svg = tree.RenderTree ()
    return Response(svg, mimetype="image/svg+xml")


# ===============================
# PREORDER
# ===============================
@app.route("/Print", methods=["POST"])
def print_preorder():
    preorder = tree.preOrder() if hasattr(tree, "preOrder") else []
    return jsonify({"preorder": preorder})


if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True, port=5000)
    with open ("Files/Typology.json" , "w" , encoding="utf-8") as f:
        data = tree.converdicc ()
        json.dump (data , f)
>>>>>>> parent of 2a9aa78 (fix: correct node attribute names in BST and update JSON formatting in Topology)
