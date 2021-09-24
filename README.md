# printex - module for pretty printing of objects.


This library is a pretty printer of python objects. A pretty printer shows the structure of an object. If the argument is a collection, then it displays the structure of each element.
This module has some similarities with [pprint](https://docs.python.org/3/library/pprint.html); however this is a new implementation.
This module also shows the field values for an argument object; if the field values are themself objects, then their structure is also shows, recursively. To me that makes much more sense than what pprint is doing.

This library works with python3.

# Installation

```pip3 install printex```

This module is on pip [link](https://pypi.org/project/printex/)

# Test program

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
```

# Output of test program

```
graph:  <class '__main__.GraphNode'> at 0x7fa2edb18cd0 fields: {
  'name' : 'root',
  'links' : [
    <class '__main__.GraphNode'> at 0x7fa2edb18bb0 fields: {
      'name' : 'node1',
      'links' : [
      ]
    },
    <class '__main__.GraphNode'> at 0x7fa2edb18a00 fields: {
      'name' : 'node2',
      'links' : [
        <class '__main__.GraphNode'> at 0x7fa2edb18910 fields: {
          'name' : 'node1.1',
          'links' : [
          ]
        },
        <class '__main__.GraphNode'> at 0x7fa2edb18730 fields: {
          'name' : 'node2.1',
          'links' : [
          ]
        },
        <Recursion on <class '__main__.GraphNode'> with id=0x7fa2edb18cd0>
      ]
    },
    <class '__main__.GraphNode'> at 0x7fa2edb18ac0 fields: {
      'name' : 'node3',
      'links' : [
        <Recursion on <class '__main__.GraphNode'> with id=0x7fa2edb18cd0>
      ]
    }
  ]
}
```

# API

- ```class pprintex.PrettyPrint( indentation_level = 0, stream = None )```
   -  constructs a pretty printer object. The amount of indentation added for each recursive level is specified by  *indentation_level*

- ```pprintex.dprint( *args, sep=' ', end='\n', file=sys.stdout, flush=False)```
    - function is a replacement for built in ```print```, all arguments other than strings are pretty printed.

- ```class pprintex.PrettyPrintCfg```
    - configuration object for the pretty printer. has the following static members.
        - ```indent_string``` default value ' '; for each indentation level displays this string, can swap this to do tabs instead
        - ```space_per_indentation_level``` - default value 2, each indentation level shows this number of indent_string instances
        - ```use_repr_for_objects``` - default False, if set to true: don't display fields for an object, use repr instead
        - ```how_nesting_prefix``` - for each line: show the nesting level.
        - ```force_repr``` - default: empty; force repr for this set of types
        - ```_dispatch``` - internal: dispatch for formatting function per type.

- ```pprintex.pformat(obj, indentation_level=0)```
    - return string that stands for pretty printed ```obj```.

