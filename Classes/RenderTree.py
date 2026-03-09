from graphviz import Digraph
class RenderTree ():

    def __init__ (self , arbol):
        self.arbol = arbol
    
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

        def AddNode(n):
            if n:
                node_id = str(id(n))
                label_text = str(n.getFlightCode())
                dot.node(node_id, label=label_text)
                if n.getLeftSon():
                    dot.edge(node_id, str(id(n.getLeftSon())))
                    AddNode(n.getLeftSon())
                if n.getRightSon():
                    dot.edge(node_id, str(id(n.getRightSon())))
                    AddNode(n.getRightSon())

        if self.arbol.root:
            AddNode(self.arbol.root)
        svg = dot.pipe(format='svg').decode("utf-8")
        return svg.replace('<svg ', '<svg width="100%" height="auto" ')