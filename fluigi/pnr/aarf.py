# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info

if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _aarf
else:
    import _aarf

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (
        self.__class__.__module__,
        self.__class__.__name__,
        strthis,
    )


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)

    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)

    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""

    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())

    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""

    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")

    __repr__ = _swig_repr
    __swig_destroy__ = _aarf.delete_SwigPyIterator

    def value(self):
        return _aarf.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _aarf.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _aarf.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _aarf.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _aarf.SwigPyIterator_equal(self, x)

    def copy(self):
        return _aarf.SwigPyIterator_copy(self)

    def next(self):
        return _aarf.SwigPyIterator_next(self)

    def __next__(self):
        return _aarf.SwigPyIterator___next__(self)

    def previous(self):
        return _aarf.SwigPyIterator_previous(self)

    def advance(self, n):
        return _aarf.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _aarf.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _aarf.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _aarf.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _aarf.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _aarf.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _aarf.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


# Register SwigPyIterator in _aarf:
_aarf.SwigPyIterator_swigregister(SwigPyIterator)

SHARED_PTR_DISOWN = _aarf.SHARED_PTR_DISOWN


class VertexVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _aarf.VertexVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _aarf.VertexVector___nonzero__(self)

    def __bool__(self):
        return _aarf.VertexVector___bool__(self)

    def __len__(self):
        return _aarf.VertexVector___len__(self)

    def __getslice__(self, i, j):
        return _aarf.VertexVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _aarf.VertexVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _aarf.VertexVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _aarf.VertexVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _aarf.VertexVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _aarf.VertexVector___setitem__(self, *args)

    def pop(self):
        return _aarf.VertexVector_pop(self)

    def append(self, x):
        return _aarf.VertexVector_append(self, x)

    def empty(self):
        return _aarf.VertexVector_empty(self)

    def size(self):
        return _aarf.VertexVector_size(self)

    def swap(self, v):
        return _aarf.VertexVector_swap(self, v)

    def begin(self):
        return _aarf.VertexVector_begin(self)

    def end(self):
        return _aarf.VertexVector_end(self)

    def rbegin(self):
        return _aarf.VertexVector_rbegin(self)

    def rend(self):
        return _aarf.VertexVector_rend(self)

    def clear(self):
        return _aarf.VertexVector_clear(self)

    def get_allocator(self):
        return _aarf.VertexVector_get_allocator(self)

    def pop_back(self):
        return _aarf.VertexVector_pop_back(self)

    def erase(self, *args):
        return _aarf.VertexVector_erase(self, *args)

    def __init__(self, *args):
        _aarf.VertexVector_swiginit(self, _aarf.new_VertexVector(*args))

    def push_back(self, x):
        return _aarf.VertexVector_push_back(self, x)

    def front(self):
        return _aarf.VertexVector_front(self)

    def back(self):
        return _aarf.VertexVector_back(self)

    def assign(self, n, x):
        return _aarf.VertexVector_assign(self, n, x)

    def resize(self, *args):
        return _aarf.VertexVector_resize(self, *args)

    def insert(self, *args):
        return _aarf.VertexVector_insert(self, *args)

    def reserve(self, n):
        return _aarf.VertexVector_reserve(self, n)

    def capacity(self):
        return _aarf.VertexVector_capacity(self)

    __swig_destroy__ = _aarf.delete_VertexVector


# Register VertexVector in _aarf:
_aarf.VertexVector_swigregister(VertexVector)


class RouteVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _aarf.RouteVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _aarf.RouteVector___nonzero__(self)

    def __bool__(self):
        return _aarf.RouteVector___bool__(self)

    def __len__(self):
        return _aarf.RouteVector___len__(self)

    def __getslice__(self, i, j):
        return _aarf.RouteVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _aarf.RouteVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _aarf.RouteVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _aarf.RouteVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _aarf.RouteVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _aarf.RouteVector___setitem__(self, *args)

    def pop(self):
        return _aarf.RouteVector_pop(self)

    def append(self, x):
        return _aarf.RouteVector_append(self, x)

    def empty(self):
        return _aarf.RouteVector_empty(self)

    def size(self):
        return _aarf.RouteVector_size(self)

    def swap(self, v):
        return _aarf.RouteVector_swap(self, v)

    def begin(self):
        return _aarf.RouteVector_begin(self)

    def end(self):
        return _aarf.RouteVector_end(self)

    def rbegin(self):
        return _aarf.RouteVector_rbegin(self)

    def rend(self):
        return _aarf.RouteVector_rend(self)

    def clear(self):
        return _aarf.RouteVector_clear(self)

    def get_allocator(self):
        return _aarf.RouteVector_get_allocator(self)

    def pop_back(self):
        return _aarf.RouteVector_pop_back(self)

    def erase(self, *args):
        return _aarf.RouteVector_erase(self, *args)

    def __init__(self, *args):
        _aarf.RouteVector_swiginit(self, _aarf.new_RouteVector(*args))

    def push_back(self, x):
        return _aarf.RouteVector_push_back(self, x)

    def front(self):
        return _aarf.RouteVector_front(self)

    def back(self):
        return _aarf.RouteVector_back(self)

    def assign(self, n, x):
        return _aarf.RouteVector_assign(self, n, x)

    def resize(self, *args):
        return _aarf.RouteVector_resize(self, *args)

    def insert(self, *args):
        return _aarf.RouteVector_insert(self, *args)

    def reserve(self, n):
        return _aarf.RouteVector_reserve(self, n)

    def capacity(self):
        return _aarf.RouteVector_capacity(self)

    __swig_destroy__ = _aarf.delete_RouteVector


# Register RouteVector in _aarf:
_aarf.RouteVector_swigregister(RouteVector)


class CellVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _aarf.CellVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _aarf.CellVector___nonzero__(self)

    def __bool__(self):
        return _aarf.CellVector___bool__(self)

    def __len__(self):
        return _aarf.CellVector___len__(self)

    def __getslice__(self, i, j):
        return _aarf.CellVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _aarf.CellVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _aarf.CellVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _aarf.CellVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _aarf.CellVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _aarf.CellVector___setitem__(self, *args)

    def pop(self):
        return _aarf.CellVector_pop(self)

    def append(self, x):
        return _aarf.CellVector_append(self, x)

    def empty(self):
        return _aarf.CellVector_empty(self)

    def size(self):
        return _aarf.CellVector_size(self)

    def swap(self, v):
        return _aarf.CellVector_swap(self, v)

    def begin(self):
        return _aarf.CellVector_begin(self)

    def end(self):
        return _aarf.CellVector_end(self)

    def rbegin(self):
        return _aarf.CellVector_rbegin(self)

    def rend(self):
        return _aarf.CellVector_rend(self)

    def clear(self):
        return _aarf.CellVector_clear(self)

    def get_allocator(self):
        return _aarf.CellVector_get_allocator(self)

    def pop_back(self):
        return _aarf.CellVector_pop_back(self)

    def erase(self, *args):
        return _aarf.CellVector_erase(self, *args)

    def __init__(self, *args):
        _aarf.CellVector_swiginit(self, _aarf.new_CellVector(*args))

    def push_back(self, x):
        return _aarf.CellVector_push_back(self, x)

    def front(self):
        return _aarf.CellVector_front(self)

    def back(self):
        return _aarf.CellVector_back(self)

    def assign(self, n, x):
        return _aarf.CellVector_assign(self, n, x)

    def resize(self, *args):
        return _aarf.CellVector_resize(self, *args)

    def insert(self, *args):
        return _aarf.CellVector_insert(self, *args)

    def reserve(self, n):
        return _aarf.CellVector_reserve(self, n)

    def capacity(self):
        return _aarf.CellVector_capacity(self)

    __swig_destroy__ = _aarf.delete_CellVector


# Register CellVector in _aarf:
_aarf.CellVector_swigregister(CellVector)


class Vertex(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    x = property(_aarf.Vertex_x_get, _aarf.Vertex_x_set)
    y = property(_aarf.Vertex_y_get, _aarf.Vertex_y_set)

    def __init__(self):
        _aarf.Vertex_swiginit(self, _aarf.new_Vertex())

    __swig_destroy__ = _aarf.delete_Vertex


# Register Vertex in _aarf:
_aarf.Vertex_swigregister(Vertex)


class Route(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _aarf.Route_swiginit(self, _aarf.new_Route(*args))

    __swig_destroy__ = _aarf.delete_Route
    start = property(_aarf.Route_start_get, _aarf.Route_start_set)
    end = property(_aarf.Route_end_get, _aarf.Route_end_set)
    waypoints = property(_aarf.Route_waypoints_get, _aarf.Route_waypoints_set)


# Register Route in _aarf:
_aarf.Route_swigregister(Route)


class Cell(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    x = property(_aarf.Cell_x_get, _aarf.Cell_x_set)
    y = property(_aarf.Cell_y_get, _aarf.Cell_y_set)
    x_span = property(_aarf.Cell_x_span_get, _aarf.Cell_x_span_set)
    y_span = property(_aarf.Cell_y_span_get, _aarf.Cell_y_span_set)

    def __init__(self):
        _aarf.Cell_swiginit(self, _aarf.new_Cell())

    __swig_destroy__ = _aarf.delete_Cell


# Register Cell in _aarf:
_aarf.Cell_swigregister(Cell)


class Router(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, obstacles, channelWidth, channelSpacing):
        _aarf.Router_swiginit(self, _aarf.new_Router(obstacles, channelWidth, channelSpacing))

    __swig_destroy__ = _aarf.delete_Router
    obstacles = property(_aarf.Router_obstacles_get, _aarf.Router_obstacles_set)
    channelWidth = property(_aarf.Router_channelWidth_get, _aarf.Router_channelWidth_set)
    channelSpacing = property(_aarf.Router_channelSpacing_get, _aarf.Router_channelSpacing_set)

    def route(self, sources, targets):
        return _aarf.Router_route(self, sources, targets)


# Register Router in _aarf:
_aarf.Router_swigregister(Router)
