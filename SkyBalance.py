from Classes.AVL import AVLTree
from Classes.FlightSB import Flight
from flask import Flask , jsonify , render_template , request, Response
from graphviz import Digraph

app = Flask (__name__)
tree = AVLTree ()

@app.route ("/")
def home ():
    try:
        grafico_svg = tree.RenderTree()
    except Exception as e:
        print(f"Error generating initial SVG: {e}")
        grafico_svg = ""
    return render_template ("index.html" , grafico = grafico_svg)

@app.route ("/Sent/Node" , methods=['POST'])
def RecibirVuelo ():
    data = request.get_json ()
    code = data.get ("code")
    origin = data.get ("origin")
    destination = data.get ("destination")
    departureTime = data.get ("departureTime")
    basePrice = data.get ("basePrice")
    numberPassengers = data.get ("numberPassengers")
    temp = Flight (code , origin , destination , departureTime , basePrice , numberPassengers , priority= False , promotion = False , alert= False)
    print (f"Hecho... Se ha agregado el vuelo {temp.code}")
    tree.insertNode (temp)
    print (f"Se ha ingresado el nodo")
    return jsonify ({"message": f"Vuelo {temp.code} agregado exitosamente"})

@app.route ("/Print" , methods = ['POST'])
def PrintPreOrder ():
    data = request.get_json ()
    print (data.get ("Hecho"))
    result = tree.preorderTour()
    print (result)
    return jsonify({"preorder": result})

@app.route ("/Render/Tree" , methods=['POST','GET'])
def RenderTree ():
    svg = tree.RenderTree()
    return Response(svg, mimetype='image/svg+xml')

if __name__ == "__main__":
    app.run(debug=True)