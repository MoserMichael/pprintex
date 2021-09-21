# printex - module for pretty printing of objects.

This module is a pretty printer of python objects. A pretty printer shows the structure of an object, if the argument is a collection then it displays the structure of each element.
This module some similarities with [pprint](https://docs.python.org/3/library/pprint.html); but this is a new implementation.
Now this module also shows the field values for argument object, if the field values are objects, then it shows these objects, recursively.  To me that makes much more sense than what pprint is doing.

# Installation

```pip install printex```

This module is on pip [link](https://pypi.org/project/printex/)

# Test program

```
import printex

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

next_ch = GraphNode("node2.1")
ch2.add_link(root)



printex.dprint("graph: ", root)
```

# Output of test program

```
graph:  <class '__main__.GraphNode'> at 0x7f861cb18df0 fields: {
  'name' : 'root',
  'links' : [
    <class '__main__.GraphNode'> at 0x7f861cb18cd0 fields: {
      'name' : 'node1',
      'links' : [
      ]
    },
    <class '__main__.GraphNode'> at 0x7f861cb18b20 fields: {
      'name' : 'node2',
      'links' : [
        <class '__main__.GraphNode'> at 0x7f861cb18a30 fields: {
          'name' : 'node1.1',
          'links' : [
          ]
        },
        <class '__main__.GraphNode'> at 0x7f861cb189a0 fields: {
          'name' : 'node2.1',
          'links' : [
          ]
        },
        <Recursion on GraphNode with id=0x7f861cb18df0>
      ]
    },
    <class '__main__.GraphNode'> at 0x7f861cb18be0 fields: {
      'name' : 'node3',
      'links' : [
        <Recursion on GraphNode with id=0x7f861cb18df0>
      ]
    }
  ]
}
```

# API

- ```class printex.PrettyPrint( indentation_level = 0, stream = None )```
   -  constructs a pretty printer object. The amount of indentation added for each recursive level is specified by  *indentation_level*

- ```printex.dprint( *args, sep=' ', end='\n', file=sys.stdout, flush=False)```
    - function is a replacement for built in ```print```, all arguments other than strings are pretty printed.

- ```class printex.PrettyPrintCfg```
    - configuration object for the pretty printer. has the following static members.
        - ```indent_string``` default value ' '; for each indentation level displays this string, can swap this to do tabs instead
        - ```space_per_indentation_level``` - default value 2, each indentation level shows this number of indent_string instances
        - ```use_repr_for_objects``` - default False, if set to true: don't display fields for an object, use repr instead
        - ```how_nesting_prefix``` - for each line: show the nesting level.
        - ```force_repr``` - default: empty; force repr for this set of types
        - ```_dispatch``` - internal: dispatch for formatting function per type.

- ```pformat(obj, indentation_level=0)```
    - return string that stands for pretty printed ```obj```.

