#!/usr/bin/env python3

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
ch2 = GraphNode("node2")
root.add_link(ch2)
ch = GraphNode("node3")
root.add_link(ch)
ch.add_link(root)

next_ch = GraphNode("node1.1")
ch2.add_link(next_ch)

next_ch = GraphNode("node2.1")
ch2.add_link(next_ch)

ch2.add_link(root)



pprintex.dprint("graph: ", root)





