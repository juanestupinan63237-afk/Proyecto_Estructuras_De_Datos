from Classes.NodeAVL import Node
from Classes.BinaryTree import BinaryTree
from Classes.FlightSB import Flight
from collections import deque
from graphviz import Digraph

class AVLTree(BinaryTree):
    """
        An advanced Binary Search Tree that implements AVL self-balancing logic and performance tracking.

        Attributes:
            balanceo_activado (bool): Flag to enable or disable automatic tree balancing.
            analyticalMetrics (dict): Counters for each type of rotation and specific tree events.
            limit (int): Threshold value used for depth penalization or tree constraints.
    """
    def __init__(self):
        """Initializes the AVL tree with default metrics, balancing enabled, and no initial limit."""
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
        """
        Sets a new threshold limit and triggers the depth penalization logic.

        Args:
            limit (int): The integer value to be set as the new tree limit.
        """
        self.limit = limit
        self.depthPenalization ()

    def getLimit (self):
        """
        Retrieves the current threshold limit of the tree.

        Returns:
            int: The current limit value.
        """
        return self.limit

    def FindNode (self , code: int):
        """
        Public interface to locate a node by its flight code using the recursive search helper.

        Args:
            code (int): The flight identification code to search for.

        Returns:
            Node: The found node object if the search is successful.
        """
        return self.__FindNode__ (self.root , code)

    def __FindNode__ (self , current_root: Node , code: int):
        """
        Internal helper that recursively searches for a node based on BST properties.

        Args:
            current_root (Node): The starting node for the current search depth.
            code (int): The flight code to compare against.

        Returns:
            Node: The matching node object.

        Raises:
            Exception: If the node is not found after traversing the relevant path.
        """
        if current_root:
            if current_root.getFlightCode () == code:
                return current_root
            elif code < current_root.getFlightCode():
                return self.__FindNode__ (current_root.getLeftSon() , code)
            elif code > current_root.getFlightCode():
                return self.__FindNode__ (current_root.getRightSon() , code)
        raise Exception ("No se ha encontrado el nodo...")

    def isBalanceActive(self):
        """
        Checks the current status of the balancing mechanism.

        Returns:
            bool: True if automatic balancing is enabled, False otherwise.
        """
        return self.balanceo_activado

    def SwitchModoEstres(self):
        """
        Toggles the balancing mode; if re-enabled, it triggers a full tree rebalancing.
        """
        self.balanceo_activado = not self.balanceo_activado
        if self.balanceo_activado:
            self.BalanceAll()
 
    def BalanceAll(self):
        """
        Triggers a full tree rebalancing by traversing all nodes and applying AVL rotations.
        """
        self.root = self.__RecursiveBalance__(self.root)
 
    def __RecursiveBalance__(self, node: Node):
        """
        Recursively visits each node in post-order to update heights and restore AVL balance.

        Args:
            node (Node): The current node being processed in the recursive traversal.

        Returns:
            Node: The new root of the subtree after all descendant nodes have been rebalanced.
        """
        if node is None:
            return None
        node.setLeftSon(self.__RecursiveBalance__(node.getLeftSon()))
        node.setRightSon(self.__RecursiveBalance__(node.getRightSon()))
        node.setHeight(1 + max(self.getHeight(node.getLeftSon()), self.getHeight(node.getRightSon())))
        return self.__rebalance(node)
 
    def ResetTree(self):
        """Clears the tree structure by removing the reference to the root node."""
        self.root = None
        self.root = None
 
    def insertNodeAVL(self, value: Flight):
        """
        Public method to insert a new flight into the AVL tree; updates the root after insertion.

        Args:
            value (Flight): The flight data object to be added to the tree.
        """
        self.root = self.__insertNodeAVL(self.root, value)
 
    def __insertNodeAVL(self, node: Node, value: Flight):
        """
        Performs a recursive BST insertion and conditionally balances the node if the flag is active.

        Args:
            node (Node): The current subtree root where the insertion is being evaluated.
            value (Flight): The flight object containing the code and data to insert.

        Returns:
            Node: The resulting node for this position (new, existing, or rotated).

        Raises:
            Exception: If a flight with the same code is already present in the tree.
        """
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
        """
        Internal logic to detect imbalances and apply simple or double rotations (LL, RR, LR, RL).

        Args:
            node (Node): The node to evaluate for height deviation between its subtrees.

        Returns:
            Node: The potentially rotated node that maintains the AVL property.
        """
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
        """
        Safely retrieves the height of a node.

        Args:
            node (Node): The node to check.

        Returns:
            int: The height of the node, or 0 if the node is None.
        """
        if node is None:
            return 0
        return node.getHeight()
 
    def deleteNode(self, codeFlight):
        """
        Searches for and removes a specific flight node from the tree by its code.

        Args:
            codeFlight (int): The identifier of the flight to be deleted.
        """
        node = self.searchNode(codeFlight)
        if node is None:
            print(f"Node {codeFlight} not found, cannot delete.")
            return
        self.root = self.__deleteNode(self.root, codeFlight)
 
    def __deleteNode(self, node: Node, code):
        """
        Recursive helper that handles the three cases of BST deletion and rebalances the tree.

        Args:
            node (Node): The current node in the traversal.
            code (int): The flight code to locate and remove.

        Returns:
            Node: The new subtree root after deletion and AVL rebalancing.
        """
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
        """
        Removes a node and all its descendants from the tree, logging the total count in metrics.

        Args:
            flightCode (int): The root code of the subtree to be cancelled.
        """
        self.root = self.__massiveCancelation(self.root, flightCode)
 
    def __massiveCancelation(self, node: Node, flightCode):
        """
        Recursive helper that prunes an entire subtree and updates cancellation metrics.

        Args:
            node (Node): The current node being inspected.
            flightCode (int): The code that triggers the mass cancellation.

        Returns:
            Node: The updated subtree root or None if the node was part of the cancelled subtree.
        """
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
        """
        Public method to calculate the total size of a subtree (including the root).

        Args:
            current_root (Node): The root of the subtree to count.

        Returns:
            int: The total number of nodes in the subtree.
        """
        return self.__CountChild__ (current_root)

    def __CountChild__ (self ,current_root: Node):
        """
        Recursive helper that counts all nodes in the given subtree using post-order traversal.

        Args:
            current_root (Node): The current node being counted.

        Returns:
            int: The sum of nodes in left and right subtrees plus one for the current node.
        """
        if current_root is not None:
            left = self.__CountChild__ (current_root.getLeftSon())
            right = self.__CountChild__ (current_root.getRightSon())
            return left + right +1
        return 0

    def __minValueNode(self, node: Node):
        """
        Locates the node with the lowest flight code value by traversing to the leftmost leaf.

        Args:
            node (Node): The starting node of the subtree to search.

        Returns:
            Node: The node containing the minimum value in that subtree.
        """
        temporal = node
        while temporal.getLeftSon() is not None:
            temporal = temporal.getLeftSon()
        return temporal
 
    def getBalance(self, node: Node):
        """
        Calculates the balance factor of a specific node to determine if it is height-balanced.

        Args:
            node (Node): The node to evaluate.

        Returns:
            int: The difference between the height of the left and right subtrees.
        """
        if node is None:
            return 0
        return self.__getHeight(node.getLeftSon()) - self.__getHeight(node.getRightSon())
 
    def rightRotate(self, node: Node):
        """
        Performs a single right rotation to balance a left-heavy subtree.

        Args:
            node (Node): The pivot node where the rotation starts (the unbalanced parent).

        Returns:
            Node: The new root of the rotated subtree.
        """
        temporal1 = node.getLeftSon()
        temporal2 = temporal1.getRightSon()
        temporal1.setRightSon(node)
        node.setLeftSon(temporal2)
        node.setHeight(1 + max(self.__getHeight(node.getLeftSon()), self.__getHeight(node.getRightSon())))
        temporal1.setHeight(1 + max(self.__getHeight(temporal1.getLeftSon()), self.__getHeight(temporal1.getRightSon())))
        return temporal1
 
    def leftRotate(self, node: Node):
        """
        Performs a single left rotation to balance a right-heavy subtree.

        Args:
            node (Node): The pivot node where the rotation starts (the unbalanced parent).

        Returns:
            Node: The new root of the rotated subtree.
        """
        temporal1 = node.getRightSon()
        temporal2 = temporal1.getLeftSon()
        temporal1.setLeftSon(node)
        node.setRightSon(temporal2)
        node.setHeight(1 + max(self.__getHeight(node.getLeftSon()), self.__getHeight(node.getRightSon())))
        temporal1.setHeight(1 + max(self.__getHeight(temporal1.getLeftSon()), self.__getHeight(temporal1.getRightSon())))
        return temporal1
 
    def depthPenalization(self):
        """
        Evaluates the entire tree to apply or remove flight alerts based on the current depth limit.
        """
        if self.limit is not None:
            self.__depthPenalization(self.root, 0)
        else:
            self.__depthPenalizationAllFalse__ (self.root)
 
    def __depthPenalization(self, node: Node, depth):
        """
        Recursively traverses the tree to mark flights with alerts if they exceed the depth limit.

        Args:
            node (Node): The current node being evaluated.
            depth (int): The current depth level in the recursive traversal.
        """
        if node is None:
            return
        if depth >= self.limit:
            node.getFlight().setAlert(True)
        else:
            node.getFlight().setAlert(False)
        self.__depthPenalization(node.getLeftSon(), depth + 1)
        self.__depthPenalization(node.getRightSon(), depth + 1)
 
    def __depthPenalizationAllFalse__ (self , current_root: Node):
        """
        Traverses the tree to clear all active alerts from flight objects.

        Args:
            current_root (Node): The current node in the traversal where the alert will be disabled.
        """
        if current_root is not None:
            current_root.getFlight().setAlert(False)
            self.__depthPenalizationAllFalse__ (current_root.getRightSon())
            self.__depthPenalizationAllFalse__ (current_root.getLeftSon())

    def getAnalyticalMetrics(self) :
        """
        Gathers and returns a comprehensive report of the tree's current state and performance history.

        Returns:
            dict: A collection of data including tree height, leaf count, rotation statistics,
                cancellation logs, and various traversal lists.
        """
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

    def __getPreorder(self, node: Node):
        """
        Generates a list of flight codes using a Pre-order traversal (Root, Left, Right).

        Args:
            node (Node): The starting node for the traversal.

        Returns:
            list: A list of flight codes in pre-order sequence.
        """
        if node is None:
            return []
        result = [node.getFlightCode()]
        result += self.__getPreorder(node.getLeftSon())
        result += self.__getPreorder(node.getRightSon())
        return result

    def __getInorder(self, node: Node):
        """
        Generates a list of flight codes using an In-order traversal (Left, Root, Right).

        Args:
            node (Node): The starting node for the traversal.

        Returns:
            list: A list of flight codes sorted by their natural BST order.
        """
        if node is None:
            return []
        result = self.__getInorder(node.getLeftSon())
        result += [node.getFlightCode()]
        result += self.__getInorder(node.getRightSon())
        return result

    def __getPostorder(self, node: Node):
        """
        Generates a list of flight codes using a Post-order traversal (Left, Right, Root).

        Args:
            node (Node): The starting node for the traversal.

        Returns:
            list: A list of flight codes in post-order sequence.
        """
        if node is None:
            return []
        result = self.__getPostorder(node.getLeftSon())
        result += self.__getPostorder(node.getRightSon())
        result += [node.getFlightCode()]
        return result

    def __getWidthTour(self) :
        """
        Executes a Level-order traversal (Breadth-First Search) using a queue.

        Returns:
            list: A list of flight codes visited level by level from top to bottom.
        """
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
        """
        Exports the entire tree structure into a dictionary format for storage or transmission.

        Returns:
            dict: A topological representation of the tree including the depth limit and all nested nodes.
        """
        return {
            "tipo": "Topology",
            "limit" : self.limit,
            "arbol": self.__serializeNode(self.root)
        }

    def __serializeNode(self, node: Node):
        """
        Recursively converts a Node and its Flight data into a nested dictionary structure.

        Args:
            node (Node): The current node to serialize.

        Returns:
            dict: A dictionary containing all flight attributes, node metrics, and children sub-trees.
        """
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
        """
        Reconstructs a Node and its children from a dictionary (Hydration process).

        Args:
            dicc (dict): The dictionary source containing flight and tree structure data.

        Returns:
            Node: A fully reconstructed Node object with updated heights and child references.
        """
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
        nodo.setHeight(1 + max(self.getHeight(nodo.getLeftSon()), self.getHeight(nodo.getRightSon())))
        return nodo

    def cargar_desde_dicc(self, dicc):
        """
        Loads the tree from a dictionary using either a fixed topology or a list of sequential insertions.

        Args:
            dicc (dict): The source dictionary containing the 'tipo' (Topology or INSERCION) and data.
        """
        if dicc["tipo"] == "Topology":
            self.root = self._dicc_a_nodo_topology(dicc["arbol"])
            self.BalanceAll()
        elif dicc["tipo"] == "INSERCION":
            self.root = None
            self.cargar_desde_dicc_inserccion(dicc["vuelos"])
        self.setLimit (dicc["limit"])

    def cargar_desde_dicc_inserccion(self, vuelos: list):
        """
        Rebuilds the tree by performing standard AVL insertions for each flight in a provided list.

        Args:
            vuelos (list): A list of dictionaries, where each entry represents a flight's data.
        """
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
        """
        Configures and initializes a Graphviz object to create a high-definition visual representation of the tree.

        Returns:
            Digraph: A Graphviz object styled with a transparent background and neon-cyan nodes.
        """
        dot = Digraph()
        dot.attr('graph', bgcolor='transparent', ranksep='1.5', nodesep='1.5' , dpi = "300")
        dot.attr('node',
            shape='circle',     
            style='filled',     
            fillcolor='#1b212c',
            color='#00f2ff',    
            fontcolor='#00f2ff',
            fontname='Arial Bold',
            fontsize='100',      # <--- Súbelo al doble (100-120)
            penwidth='3',        # Un poco más grueso para que no se pierda el borde
            width='1.5',         # Aumenta el ancho mínimo
            height='1.5',        # Aumenta el alto mínimo
            fixedsize='false'    # Mantenlo en false
            )

        dot.attr('edge', color='#444d5e', penwidth='1.5', arrowhead='vee', arrowsize='0.8')

        def AddNode(n: Node):
            """
        Helper function for Render that recursively adds nodes and edges to the Graphviz object.

        It applies conditional styling: if a flight has an active alert, the node is rendered 
        in an orange/dark theme to highlight issues.

        Args:
            n (Node): The current node to be processed and added to the visual graph.
        """
            if n:
                if self.balanceo_activado is False:
                    node_id = str(id(n))
                    label_text = f"{n.getFlight().getCode()}\nBalance Factor : {self.getBalance(n)}\nOrigin: {n.getFlight().getOrigin()}\ndestination: {n.getFlight().getDestination()}\nTotal Price: {n.getFlight().getTotalPrice()}"
                    if not n.getFlight().getAlert ():
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
                    label_text = f"Code: {n.getFlightCode()}\nOrigin: {n.getFlight().getOrigin()}\ndestination: {n.getFlight().getDestination()}\nTotal Price: {n.getFlight().getTotalPrice()}"
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
        """
        Identifies the flight with the lowest total price using a recursive search.

        Tie-breaking logic: If prices are equal, it prefers the node at a greater depth.
        If depths are also equal, it selects the node with the higher flight code.

        Returns:
            Node: The node identified as the least profitable based on the defined criteria.
        """
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
        """
        Locates the least profitable flight in the tree and removes its node.
        """
        code = self.FindNodeLessProfitable ().getFlightCode ()
        self.deleteNode (code)

    def TourInsertion (self , code: int):
        """
        Retrieves a list of all flight objects in the subtree starting from a specific flight code.

        Args:
            code (int): The flight code of the node to use as the root for the traversal.

        Returns:
            list[Flight]: A list of Flight objects found in the specified subtree.
        """
        nodo = self.FindNode (code)
        return self.__TourInsertion__ (nodo)

    def __TourInsertion__ (self, current_root: Node , resultado = []):
        """
        Recursively collects Flight objects from a subtree using a pre-order approach.

        Args:
            current_root (Node): The current node in the traversal.
            resultado (list, optional): The accumulator list for flight objects.

        Returns:
            list[Flight]: The accumulated list of flights.
        """
        if resultado is None:
            resultado = []
        if current_root:
            resultado.append (current_root.getFlight())
            self.__TourInsertion__ (current_root.getLeftSon())
            self.__TourInsertion__ (current_root.getRightSon())
        return resultado

    def InsertionSave (self):
        """
        Generates a serializable dictionary specifically formatted for the 'INSERCION' load mode.

        Returns:
            dict: A dictionary containing the tree type, depth limit, and a list of flight data.
        """
        vuelos = []
        self.__InsertionSave__ (self.root , vuelos)
        return {"tipo" : "INSERCION",
                "limit" : self.limit,
                "vuelos" : vuelos}

    def __InsertionSave__ (self , current_root: Node , resultado: list[dict]):
        """
        Recursive helper that flattens the tree into a list of flight dictionaries.

        Args:
            current_root (Node): The current node being serialized.
            resultado (list[dict]): The list where flight data dictionaries are appended.
        """
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
        """
        Locates a node by its original code and updates its internal Flight object.

        Args:
            code (int): The current flight code of the node to be edited.
            flight (Flight): The new Flight object to be assigned to the node.
        """
        self.__EditFligth__ (self.root , code , fligth)

    def __EditFligth__ (self ,current_root: Node , code: int , fligth : Flight):
            """
        Recursive helper that navigates the BST to find the target node for editing.

        Args:
            current_root (Node): The current node in the search path.
            code (int): The identifier to search for.
            flight (Flight): The updated data to set if the code matches.
        """
            if current_root:
                if current_root.getFlightCode () == code:
                    current_root.setFlight (fligth)
                    return
                if code < current_root.getFlightCode():
                    self.__EditFligth__ (current_root.getLeftSon() , code , fligth)
                if code > current_root.getFlightCode():
                    self.__EditFligth__ (current_root.getRightSon() , code , fligth)