from Classes.BSTTree import BST
from Classes.FlightSB import Flight
from flask import Flask, jsonify, render_template, request, Response

app = Flask(__name__)

tree = BST()

@app.route("/")
def home():
    grafico_svg = tree.RenderTree()
    return render_template("index.html", grafico=grafico_svg)

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

        tree.insertNode(nuevo_vuelo)

        return jsonify({
            "status": "success",
            "message": f"Vuelo {code} registrado correctamente"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/Render/Tree", methods=['GET'])
def RenderTreeRoute():
    svg = tree.RenderTree()
    return Response(svg, mimetype='image/svg+xml')

if __name__ == "__main__":
    app.run(debug=True, port=5000)