
import pprintex

class Node:
    def __init__(self, name):
        self.name = name

class GraphNode(Node):
    def __init__(self, node_name):
        super(GraphNode, self).__init__(node_name)
        self.links = []

    def add_link(self, node):
        self.links.append(node)

root = GraphNode("root")
ch = GraphNode("node1")
root.add_link(ch)
ch = GraphNode("node2")
root.add_link(ch)
ch = GraphNode("node3")
root.add_link(ch)
ch.add_link(root)

pprintex.Print("graph", root)





