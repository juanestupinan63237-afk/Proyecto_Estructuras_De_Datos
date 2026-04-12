from Classes.NodeAVL import Node
from Classes.BinaryTree import BinaryTree
from Classes.FlightSB import Flight
from collections import deque
from graphviz import Digraph

class AVLTree(BinaryTree):
 
    def __init__(self):
        super().__init__()
        self.balanceo_activado = True
        self.analyticalMetrics = {
            "simpleLeft": 0,
            "simpleRight": 0,
            "doubleLeft": 0,
            "doubleRight": 0,
            "massCancellations": 0
        }
        self.limit = None

    def setLimit (self, limit: int):
        self.limit = limit
        self.depthPenalization ()

    def getLimit (self):
        return self.limit

    def FindNode (self , code: int):
        return self.__FindNode__ (self.root , code)

    def __FindNode__ (self , current_root: Node , code: int):
        if current_root:
            if current_root.getFlightCode () == code:
                return current_root
            elif code < current_root.getFlightCode():
                return self.__FindNode__ (current_root.getLeftSon() , code)
            elif code > current_root.getFlightCode():
                return self.__FindNode__ (current_root.getRightSon() , code)
        raise Exception ("No se ha encontrado el nodo...")
 
    def isBalanceActive(self):
        return self.balanceo_activado
 
    def SwitchModoEstres(self):
        self.balanceo_activado = not self.balanceo_activado
        if self.balanceo_activado:
            self.BalanceAll()
 
    def BalanceAll(self):
        self.root = self.__RecursiveBalance__(self.root)
 
    def __RecursiveBalance__(self, node: Node):
        if node is None:
            return None
        node.setLeftSon(self.__RecursiveBalance__(node.getLeftSon()))
        node.setRightSon(self.__RecursiveBalance__(node.getRightSon()))
        node.setHeight(1 + max(self.getHeight(node.getLeftSon()),
                               self.getHeight(node.getRightSon())))
        return self.__rebalance(node)
 
    def ResetTree(self):
        self.root = None
 
    def insertNodeAVL(self, value: Flight):
        self.root = self.__insertNodeAVL(self.root, value)
 
    def __insertNodeAVL(self, node: Node, value: Flight):
        if node is None:
            return Node(value)
        if value.getCode() < node.getFlightCode():
            node.setLeftSon(self.__insertNodeAVL(node.getLeftSon(), value))
        elif value.getCode() > node.getFlightCode():
            node.setRightSon(self.__insertNodeAVL(node.getRightSon(), value))
        else:
            raise Exception("This Node already exists in our AVL Tree...")
        node.setHeight(1 + max(self.getHeight(node.getLeftSon()), self.getHeight(node.getRightSon())))
        if self.balanceo_activado:
            return self.__rebalance(node)
        return node
 
    def __rebalance(self, node: Node):
        if node is None:
            return None
        node.setHeight(1 + max(self.__getHeight(node.getLeftSon()), self.__getHeight(node.getRightSon())))
        balance = self.getBalance(node)
        if balance > 1:
            if self.getBalance(node.getLeftSon()) >= 0:
                self.analyticalMetrics["simpleRight"] += 1
                return self.rightRotate(node)
            else:
                self.analyticalMetrics["doubleRight"] += 1
                node.setLeftSon(self.leftRotate(node.getLeftSon()))
                return self.rightRotate(node)
        if balance < -1:
            if self.getBalance(node.getRightSon()) <= 0:
                self.analyticalMetrics["simpleLeft"] += 1
                return self.leftRotate(node)
            else:
                self.analyticalMetrics["doubleLeft"] += 1
                node.setRightSon(self.rightRotate(node.getRightSon()))
                return self.leftRotate(node)
        return node
 
    def __getHeight(self, node: Node):
        if node is None:
            return 0
        return node.getHeight()
 
    def deleteNode(self, codeFlight):
        node = self.searchNode(codeFlight)
        if node is None:
            print(f"Node {codeFlight} not found, cannot delete.")
            return
        self.root = self.__deleteNode(self.root, codeFlight)
 
    def __deleteNode(self, node: Node, code):
        if node is None:
            return node
        if code < node.getFlightCode():
            node.setLeftSon(self.__deleteNode(node.getLeftSon(), code))
        elif code > node.getFlightCode():
            node.setRightSon(self.__deleteNode(node.getRightSon(), code))
        else:
            if node.getLeftSon() is None and node.getRightSon() is None:
                return None
            elif node.getRightSon() is None:
                return node.getLeftSon()
            elif node.getLeftSon() is None:
                return node.getRightSon()
            else:
                successor = self.__minValueNode(node.getRightSon())
                node.setFlight(successor.getFlight())
                node.setRightSon(self.__deleteNode(node.getRightSon(), successor.getFlight().getCode()))
        return self.__rebalance(node)
 
    def massiveCancelation(self, flightCode):
        self.root = self.__massiveCancelation(self.root, flightCode)
 
    def __massiveCancelation(self, node: Node, flightCode):
        if node is None:
            return None
        if flightCode < node.getFlightCode():
            node.setLeftSon(self.__massiveCancelation(node.getLeftSon(), flightCode))
        elif flightCode > node.getFlightCode():
            node.setRightSon(self.__massiveCancelation(node.getRightSon(), flightCode))
        else:
            self.analyticalMetrics["massCancellations"] += self.CountChilds (node)
            return None
        return self.__rebalance(node)
 
    def CountChilds (self, current_root: Node):
        return self.__CountChild__ (current_root) 

    def __CountChild__ (self ,current_root: Node):
        if current_root is not None:
            izq = self.__CountChild__ (current_root.getLeftSon())
            der = self.__CountChild__ (current_root.getRightSon())
            return izq + der +1
        return 0

    def __minValueNode(self, node: Node):
        temporal = node
        while temporal.getLeftSon() is not None:
            temporal = temporal.getLeftSon()
        return temporal
 
    def getBalance(self, node: Node):
        if node is None:
            return 0
        return self.__getHeight(node.getLeftSon()) - self.__getHeight(node.getRightSon())
 
    def rightRotate(self, node: Node):
        temporal1 = node.getLeftSon()
        temporal2 = temporal1.getRightSon()
        temporal1.setRightSon(node)
        node.setLeftSon(temporal2)
        node.setHeight(1 + max(self.__getHeight(node.getLeftSon()), self.__getHeight(node.getRightSon())))
        temporal1.setHeight(1 + max(self.__getHeight(temporal1.getLeftSon()), self.__getHeight(temporal1.getRightSon())))
        return temporal1
 
    def leftRotate(self, node: Node):
        temporal1 = node.getRightSon()
        temporal2 = temporal1.getLeftSon()
        temporal1.setLeftSon(node)
        node.setRightSon(temporal2)
        node.setHeight(1 + max(self.__getHeight(node.getLeftSon()), self.__getHeight(node.getRightSon())))
        temporal1.setHeight(1 + max(self.__getHeight(temporal1.getLeftSon()), self.__getHeight(temporal1.getRightSon())))
        return temporal1
 
    def depthPenalization(self):
        if self.limit is not None:
            self.__depthPenalization(self.root, 0)
        else:
            self.__depthPenalizationAllFalse__ (self.root)
 
    def __depthPenalization(self, node: Node, depth):
        if node is None:
            return
        if depth >= self.limit:
            node.getFlight().setAlert(True)
        else:
            node.getFlight().setAlert(False)
        self.__depthPenalization(node.getLeftSon(), depth + 1)
        self.__depthPenalization(node.getRightSon(), depth + 1)
 
    def __depthPenalizationAllFalse__ (self , current_root: Node):
        if current_root is not None:
            current_root.getFlight().setAlert(False)
            self.__depthPenalizationAllFalse__ (current_root.getRightSon())
            self.__depthPenalizationAllFalse__ (current_root.getLeftSon())

    def getAnalyticalMetrics(self) :
        return {
            "height":            self.getHeight(self.root),
            "leaves":            self.countLeaves(),
            "rotations": {
                "simpleLeft":    self.analyticalMetrics["simpleLeft"],
                "simpleRight":   self.analyticalMetrics["simpleRight"],
                "doubleLeft":    self.analyticalMetrics["doubleLeft"],
                "doubleRight":   self.analyticalMetrics["doubleRight"],
                "total":         sum([
                                     self.analyticalMetrics["simpleLeft"],
                                     self.analyticalMetrics["simpleRight"],
                                     self.analyticalMetrics["doubleLeft"],
                                     self.analyticalMetrics["doubleRight"],
                                 ])
            },
            "massCancellations": self.analyticalMetrics["massCancellations"],
            "traversals": {
                "preorder":  self.__getPreorder(self.root),
                "inorder":   self.__getInorder(self.root),
                "postorder": self.__getPostorder(self.root),
                "width":     self.__getWidthTour(),
            }
        }

    def __getPreorder(self, node: Node) :
        if node is None:
            return []
        result = [node.getFlightCode()]
        result += self.__getPreorder(node.getLeftSon())
        result += self.__getPreorder(node.getRightSon())
        return result

    def __getInorder(self, node: Node) :
        if node is None:
            return []
        result = self.__getInorder(node.getLeftSon())
        result += [node.getFlightCode()]
        result += self.__getInorder(node.getRightSon())
        return result

    def __getPostorder(self, node: Node) :
        if node is None:
            return []
        result = self.__getPostorder(node.getLeftSon())
        result += self.__getPostorder(node.getRightSon())
        result += [node.getFlightCode()]
        return result

    def __getWidthTour(self) :
        if self.root is None:
            return []
        result = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.getFlightCode())
            if node.getLeftSon():
                queue.append(node.getLeftSon())
            if node.getRightSon():
                queue.append(node.getRightSon())
        return result

    def SaveTree(self) :
        return {
            "tipo": "Topology",
            "limit" : self.limit,
            "arbol": self.__serializeNode(self.root)
        }

    def __serializeNode(self, node: Node):
        if node is None:
            return None
        f = node.getFlight()
        return {
            "codigo":     f.getCode(),
            "origen":     f.getOrigin(),
            "destino":    f.getDestination(),
            "horaSalida": f.getDepartureTime(),
            "precioBase": f.getBasePrice(),
            "pasajeros":  f.getNumberPassengers(),
            "prioridad":  f.getPriority(),
            "promocion":  f.getPromotion(),
            "alerta":     f.getAlert(),
            "altura":     node.getHeight(),
            "balance":    self.getBalance(node),
            "izquierdo":  self.__serializeNode(node.getLeftSon()),
            "derecho":    self.__serializeNode(node.getRightSon()),
        }

    def _dicc_a_nodo_topology(self, dicc: dict):
        if dicc is None:
            return None
        nodo = Node(Flight(
            int(dicc["codigo"]),
            dicc["origen"],
            dicc["destino"],
            dicc["horaSalida"],
            dicc["precioBase"],
            dicc["pasajeros"],
            promotion=bool(dicc["promocion"]),
            alert=bool(dicc["alerta"]),
            priority=False
        ))
        nodo.setLeftSon(self._dicc_a_nodo_topology(dicc["izquierdo"]))
        nodo.setRightSon(self._dicc_a_nodo_topology(dicc["derecho"]))
        nodo.setHeight(1 + max(self.getHeight(nodo.getLeftSon()),
                               self.getHeight(nodo.getRightSon())))
        return nodo

    def cargar_desde_dicc(self, dicc):
        if dicc["tipo"] == "Topology":
            self.root = self._dicc_a_nodo_topology(dicc["arbol"])
            self.BalanceAll()
        elif dicc["tipo"] == "INSERCION":
            self.root = None
            self.cargar_desde_dicc_inserccion(dicc["vuelos"])
        self.setLimit (dicc["limit"])

    def cargar_desde_dicc_inserccion(self, vuelos: list):
        for i in vuelos:
            self.insertNodeAVL(Flight(
                int(i["codigo"]),
                i["origen"],
                i["destino"],
                i["horaSalida"],
                int(i["precioBase"]),
                int(i["pasajeros"]),
                int(i["prioridad"]),
                i["promocion"],
                i["alerta"]
            ))

    def Render (self):
        dot = Digraph()
        dot.attr('graph', bgcolor='transparent', ranksep='0.6', nodesep='0.4')
        dot.attr('node',
                shape='circle',     
                style='filled',     
                fillcolor='#1b212c',
                color='#00f2ff',    
                fontcolor='#00f2ff',
                fontname='Arial Bold',
                fontsize='12',
                penwidth='2',     
                width='0.6',        
                height='0.6')
        dot.attr('edge', color='#444d5e', penwidth='1.5', arrowhead='vee', arrowsize='0.8')

        def AddNode(n: Node):
            if n:
                if self.balanceo_activado is False:
                    node_id = str(id(n))
                    label_text = f"{n.getFlight().getCode()}\nBalance Factor : {self.getBalance(n)}\nOrigin: {n.getFlight().getOrigin()}\ndestination: {n.getFlight().getDestination()}\nTotal Price: {n.getFlight().getTotalPrice()}"
                    if n.getFlight().getAlert () is False:
                        dot.node(node_id, label=label_text)
                    else:
                        dot.node(node_id, label=label_text,
                            fillcolor='#3d1f00',
                            color='#ff8c00',
                            fontcolor='#ff8c00')
                    if n.getLeftSon():
                        dot.edge(node_id, str(id(n.getLeftSon())))
                        AddNode(n.getLeftSon())
                    if n.getRightSon():
                        dot.edge(node_id, str(id(n.getRightSon())))
                        AddNode(n.getRightSon())
                else:
                    node_id = str(id(n))
                    label_text = f"Origin: {n.getFlight().getOrigin()}\ndestination: {n.getFlight().getDestination()}\nTotal Price: {n.getFlight().getTotalPrice()}"
                    if n.getFlight().getAlert () is False:
                        dot.node(node_id, label=label_text)
                    else:
                        dot.node(node_id, label=label_text,
                            fillcolor='#3d1f00',
                            color='#ff8c00',
                            fontcolor='#ff8c00')
                    if n.getLeftSon():
                        dot.edge(node_id, str(id(n.getLeftSon())))
                        AddNode(n.getLeftSon())
                    if n.getRightSon():
                        dot.edge(node_id, str(id(n.getRightSon())))
                        AddNode(n.getRightSon())

        if self.root:
            AddNode(self.root)
        svg = dot.pipe(format='svg').decode("utf-8")
        return svg.replace('<svg ', '<svg width="100%" height="auto" ')

    def FindNodeLessProfitable (self):
        FLIGHT = self.root
        PROFUNDIDAD = 0
        def __Find__ (current_root: Node  , profundidad_actual = 0):
            nonlocal FLIGHT
            nonlocal PROFUNDIDAD
            if current_root is not None:
                if current_root.getFlight ().getTotalPrice () <= FLIGHT.getFlight().getTotalPrice():
                    if current_root.getFlight ().getTotalPrice() == FLIGHT.getFlight().getTotalPrice():
                        if profundidad_actual > PROFUNDIDAD:
                            FLIGHT = current_root
                            PROFUNDIDAD = profundidad_actual
                        elif profundidad_actual == PROFUNDIDAD:
                            if current_root.getFlightCode () > FLIGHT.getFlightCode():
                                FLIGHT = current_root
                                PROFUNDIDAD = profundidad_actual
                    else:
                        FLIGHT = current_root
                        PROFUNDIDAD = profundidad_actual 
                __Find__ (current_root.getLeftSon() , profundidad_actual+1)
                __Find__ (current_root.getRightSon(), profundidad_actual+1) 
        __Find__ (self.root)
        return FLIGHT

    def DeleteFligthLessProfitable (self):
        code = self.FindNodeLessProfitable ().getFlightCode ()
        self.deleteNode (code)

    def TourInsertion (self , code: int):
        nodo = self.FindNode (code)
        return self.__TourInsertion__ (nodo)

    def __TourInsertion__ (self, current_root: Node , resultado = []):
        if resultado is None:
            resultado = []
        if current_root:
            resultado.append (current_root.getFlight())
            self.__TourInsertion__ (current_root.getLeftSon())
            self.__TourInsertion__ (current_root.getRightSon())
        return resultado

    def InsertionSave (self):
        vuelos = []
        self.__InsertionSave__ (self.root , vuelos)
        return {"tipo" : "INSERCION",
                "limit" : self.limit,
                "vuelos" : vuelos}

    def __InsertionSave__ (self , current_root: Node , resultado: list[dict]):
        if current_root:
            vuelo = current_root.getFlight ()
            resultado.append ({
                "codigo" : vuelo.getCode(),
                "origen" : vuelo.getOrigin(),
                "destino" : vuelo.getDestination (),
                "horaSalida" : vuelo.getDepartureTime(),
                "precioBase" : vuelo.getBasePrice(),
                "pasajeros" : vuelo.getNumberPassengers(),
                "prioridad" : vuelo.getPriority(),
                "promocion" : vuelo.getPromotion(),
                "alerta" : vuelo.getAlert()              
            })
            self.__InsertionSave__ (current_root.getLeftSon() , resultado)
            self.__InsertionSave__ (current_root.getRightSon() , resultado)

    def EditFligth (self , code: int , fligth: Flight):
        self.__EditFligth__ (self.root , code , fligth)

    def __EditFligth__ (self ,current_root: Node , code: int , fligth : Flight):
            if current_root:
                if current_root.getFlightCode () == code:
                    current_root.setFlight (fligth)
                    return
                if code < current_root.getFlightCode():
                    self.__EditFligth__ (current_root.getLeftSon() , code , fligth)
                if code > current_root.getFlightCode():
                    self.__EditFligth__ (current_root.getRightSon() , code , fligth)