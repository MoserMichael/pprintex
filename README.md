# pprintex - module for pretty printing of objects.

This module is based on python module [pprint](https://docs.python.org/3/library/pprint.html), I copied the sources and made some modifications.

The change is as follows: pprintex also shows the field values, for each object that is pretty printed.

The module exports the same functions as pprint, it also adds the ```dprint``` function, which is quite similar to the built-in [print](https://docs.python.org/3/library/functions.html#print) function, with the difference that object arguments are pretty printed.


# test program

```
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

pprintex.dprint("graph: ", root)
```

# output of test program

```
graph:  {'links': [<class '__main__.GraphNode'> at 0x7f8aac43bf70 fields: {'links': [], 'name': 'node1'},
           <class '__main__.GraphNode'> at 0x7f8aac43bee0 fields: {'links': [], 'name': 'node2'},
           <class '__main__.GraphNode'> at 0x7f8aac43bd60 fields: {'links': [<class '__main__.GraphNode'> at 0x7f8aac43bfd0 fields: <Recursion on dict with id=140233570241280>], 'name': 'node3'}],
 'name': 'root'}
```


