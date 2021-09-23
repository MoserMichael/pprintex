

import sys
import collections
import types
import io

__all__ = [ "dprint", "pformat", "PrettyPrintCfg", "PrettyPrint" ]


# like built-in print, this one pretty prints all object arguments
# can't redefine builtin print function, so rename it to dprint
def dprint(*args, sep=' ', end='\n', indentation_level = 0, file=sys.stdout, flush=False):
    to_print = sep.join(map(lambda arg : pformat(arg) if not isinstance(arg, str) else str(arg), args))
    print(to_print, end=end, file=file, flush=flush)


class PrettyPrintCfg:
    # for each indentation level displays this string, can swap this to do tabs insteads
    indent_string = ' ' 

    # each indentation level shows this number of indent_string instances
    space_per_indent_level = 2

    # if set to true: don't display fields for an object, use repr instead
    use_repr_for_objects = False

    # for each line: show the nesting level.
    show_nesting_prefix = False

    # functions to format per type repr 
    _dispatch = {}

    # force use of repr for these types
    force_repr = set()

    # internal: builtin types
    builtin_scalars = frozenset({str, bytes, bytearray, int, float, complex,
                              bool, type(None)})


                                


def pformat(obj, indentation_level=0):
    return  PrettyPrint(indentation_level=indentation_level).pformat(obj)

def _recursion(object):
    return ("<Recursion on %s with id=%s>"
            % (str(type(object)), hex(id(object))))

def _indent_string(indentation_level):
    prefix = "(" + str(indentation_level) + ")" if PrettyPrintCfg.show_nesting_prefix else ''
    return  prefix + PrettyPrintCfg.indent_string * indentation_level * PrettyPrintCfg.space_per_indent_level

class PrettyPrint:
    def __init__(self, indentation_level=0, stream = None):
        if stream is not None:
            self._stream = stream
        else:
            self._stream = sys.stdout
        if indentation_level < 0:
            raise ValueError('indent must be >= 0')
        self._indent = indentation_level
        self._context = dict()

  
    def pformat(self, obj):
        self._stream = io.StringIO()
        self._pformat(obj, 0, False)
        return self._stream.getvalue()

    def _pformat(self, obj, indentation_level, show_leading_spaces):

        #print("type: ", type(obj), " indent: ", indentation_level, " repr: ", repr(obj))

        objid = id(obj)

        repr_str = None
        if objid in self._context:
            repr_str = _recursion(obj)
        else:
            self._context[objid] = 1

            typ = type(obj)
            if typ in PrettyPrintCfg.builtin_scalars or typ in PrettyPrintCfg.force_repr:
                repr_str = repr(obj)
            else:
                p = PrettyPrintCfg._dispatch.get(type(obj).__repr__, None)
                if p:
                    p(self, obj, indentation_level, show_leading_spaces)

                else:
                    object_dict = getattr(obj, "__dict__", None)
                    if object_dict != None:
                        indent = _indent_string(indentation_level) if show_leading_spaces else ''

                        if PrettyPrintCfg.use_repr_for_objects and getattr(typ, "__repr__", None) != None:
                            title = indent + repr(object)
                            self._stream.write(title)
                        else:
                            title = indent + str(type(obj)) +  " at " + hex(id(obj)) +  " fields: "
                            self._stream.write(title) 
                            self._pformat(object_dict, indentation_level, False)
                    else:
                        repr_str = repr(obj)

            del self._context[objid]

        if repr_str:
            self._show_repr(repr_str, indentation_level, show_leading_spaces)
           


    def _show_repr(self, repr, indentation_level, show_leading_spaces):
        indent = _indent_string(indentation_level)
        lines = repr.splitlines()
        last_index = len(lines) - 1

        for idx, line in enumerate(lines):
            if (idx == 0 and show_leading_spaces) or idx != 0:
                self._stream.write(indent)
            self._stream.write(line)
            if idx != last_index:
                self._stream.write('\n')
  
    def _pprint_dict(self, object, indentation_level, show_leading_spaces):
        write = self._stream.write
        indent = _indent_string(indentation_level)

        if show_leading_spaces:
            write(indent)

        if not isinstance(object, dict):
             write(str(type(object)))
             write('(')
        write('{\n')

        items = object.items()
        last_index = len(items) - 1

        for i, (key, value) in enumerate(items):
            self._show_repr(repr(key), indentation_level + 1, True)
            write(" : ")
            self._pformat(value, indentation_level + 1, False)
            if i != last_index:
                write(",")
            write("\n")
        
        write(indent)
        if not isinstance(object, dict):
            write(')')
        write('}')

    def _pprint_list(self, object, indentation_level, show_leading_spaces):
        write = self._stream.write
        indent = _indent_string(indentation_level)

        if show_leading_spaces:
            write(indent)

        if not isinstance(object, list) and not isinstance(object, tuple):
             write(str(type(object)))
             write('(')

        if isinstance(object, tuple):
            write('(\n')
        else:
            write('[\n')

        self._format_items(object, indentation_level + 1)
        
        if isinstance(object, tuple):
            write(indent + ')')
        else:
            write(indent + ']')

        if not isinstance(object, list) and not isinstance(object, tuple):
             write(')')

    def _format_items(self, object, indentation_level):
        write = self._stream.write
        indent = _indent_string(indentation_level)

        items = iter(object)
        last_index = len(object) - 1

        for i, item in enumerate(items):
        
            self._pformat( item, indentation_level, True)

            if i != last_index:
                write(",")
            write("\n")

    def _print_user_obj(self, object, indentation_level, show_leading_spaces):
        self._pformat(object.data, indentation_level, show_leading_spaces)

    def _print_mappingproxy(self, object, indentation_level, show_leading_spaces):
        print("mappingobjid:", hash(id(object.copy())))
        self._pformat(object.copy(), indentation_level, show_leading_spaces)


def init_dict():
    PrettyPrintCfg._dispatch[dict.__repr__] = PrettyPrint._pprint_dict
    PrettyPrintCfg._dispatch[collections.UserDict.__repr__] = PrettyPrint._pprint_dict
    PrettyPrintCfg._dispatch[collections.OrderedDict.__repr__] = PrettyPrint._pprint_dict
    PrettyPrintCfg._dispatch[collections.Counter.__repr__] = PrettyPrint._pprint_dict
    PrettyPrintCfg._dispatch[types.MappingProxyType.__repr__] = PrettyPrint._print_mappingproxy
    
    PrettyPrintCfg._dispatch[list.__repr__] = PrettyPrint._pprint_list
    PrettyPrintCfg._dispatch[collections.deque.__repr__] = PrettyPrint._pprint_list
    PrettyPrintCfg._dispatch[tuple.__repr__] = PrettyPrint._pprint_list
    PrettyPrintCfg._dispatch[set.__repr__] = PrettyPrint._pprint_list
    PrettyPrintCfg._dispatch[frozenset.__repr__] = PrettyPrint._pprint_list

    PrettyPrintCfg._dispatch[collections.UserList.__repr__] = PrettyPrint._print_user_obj
    PrettyPrintCfg._dispatch[collections.UserString.__repr__] = PrettyPrint._print_user_obj


init_dict()















