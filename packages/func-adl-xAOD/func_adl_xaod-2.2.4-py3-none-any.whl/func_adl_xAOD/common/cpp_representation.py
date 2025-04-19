from __future__ import annotations

# The representation, in C++ code, of all the data being passed around the system by the C++
# code. Mostly, these are used as "representations" of a particular AST node. Here is an outline
# of how this works:
#
# Things are broken down, generally, into values and sequences.
#
# A value is something like j->pt(), or perhaps even just j. It has a specific value, and it
# also has a particular place where it is valid - the so-called scope. The scope tells you exactly
# where in the code you are allowed to refer to that value. The value is valid at that scope or
# anything deeper.
#
# A collection is a special type of value. The thing about collection is that you can turn it into
# a sequence. This happens implicitly with code that looks like "e.Jets.Select(xxx)" - between the Jets
# and the Select, the collection that is e.Jets gets turned into a sequence.
#
# A tuple is just a special case of a value, and it contains a series of either values or sequences or collections, etc.
#
# Finally, a sequence is something we are iterating over. Select, SelectMany, and Where all return sequences.
# A sequence has the loop iterator - the thing that we are looping over. This iterator is just a value, and has
# all the properties of a value. A sequence also has a "value" associated with it. This value is at first just
# the iterator. But you can have something like a select statement that will do Select(j->pT()). In that case
# the sequence value transforms from j to j->pT(). THe iterator value remains the same at that point.
#
# It is instructive to talk about how various LINQ predicates transform the above things.
#
# seq.Select(f(x)):
#  - if seq is a collection -> sequence with a new iterator value and the sequence value being f(iterator value)
#  - seq can't be a plain value
#  - if seq is a sequence -> new sequence with same iterator value and sequence value being f(old sequence value).
#    Note it is possible for the sequence value to be another sequence!
#
# seq.SelectMany(f(x)):
#  - if seq is a collection -> sequence with a new iterator value and sequence value being f(iterator value).
#    Then go onto next step that applies.
#  - seq can't be a plane value
#
#  next look a the sequence value:
#  - collection -> start a new sequence with the iterator and sequence value being the iterator
#  - value -> not allowedNone,
#  - sequence -> keep the sequence
#
# seq.First()
#  - seq is a collection -> start a new sequence with the iterator and sequence being the iterator
#  - seq is a value -> not allowed
# then
#  - seq is a sequence -> return the sequence value
#
# Others follow a similar line of reasoning.
import ast
import copy
from typing import Any, Optional, TypeVar, Union, cast

import func_adl_xAOD.common.cpp_types as ctyp
from func_adl_xAOD.common.util_scope import gc_scope, gc_scope_top_level


class dummy_ast(ast.AST):
    "A dummy ast"

    _fields = tuple()

    def __init__(self, node: cpp_rep_base):
        set_rep(self, node)


class cpp_rep_base:
    r"""
    Represents a term or collection in C++ code. Base class for all values, collections, sequences.

    This is an abstract class for the most part. Do not override things that aren't needed - that way the system will
    know when the user tries to do something that they shouldn't have.

    We know only about our type
    """

    def __init__(self):
        pass

    def as_ast(self):
        "Create an AST rep of this guy"
        return dummy_ast(self)


class cpp_namespace(cpp_rep_base):
    def __init__(self, ns: ctyp.NameSpaceInfo):
        """Create a representation of a namespace in C++ code"""
        self._ns = ns

    def __str__(self) -> str:
        return f"cpp_namespace({self._ns.full_name})"

    def scope(self) -> gc_scope_top_level:
        return gc_scope_top_level()

    @property
    def ns(self) -> ctyp.NameSpaceInfo:
        return self._ns


class cpp_enum(cpp_rep_base):
    def __init__(self, enum: ctyp.ENumInfo):
        """Create a representation of a enum in C++ code"""
        self._enum = enum

    def __str__(self) -> str:
        return f"cpp_enum({self._enum.full_name})"

    def scope(self) -> gc_scope_top_level:
        return gc_scope_top_level()

    @property
    def enum(self) -> ctyp.ENumInfo:
        return self._enum


class cpp_value(cpp_rep_base):
    r"""
    Represents a value. This has a particular value in C++ code that is valid at some C++ scope, or deeper.
    """

    def __init__(
        self,
        cpp_expression: str,
        scope: Optional[Union[gc_scope, gc_scope_top_level]],
        cpp_type: Optional[ctyp.terminal],
    ):
        r"""
        Initialize a C++ value

        cpp_expression:         The C++ name that can be emitted to code
        scope:                  The scope at which this value is valid
        cpp_type:               Type that we can deal with
        """
        cpp_rep_base.__init__(self)
        self._scope = scope
        self._expression = cpp_expression
        assert not isinstance(cpp_type, str)
        self._cpp_type = cpp_type

    def __str__(self) -> str:
        return f"{str(self._cpp_type)} value (expression {self._expression})"

    @property
    def p_depth(self) -> int:
        "Return the depth of the pointer"
        return self.cpp_type().p_depth

    def as_cpp(self) -> str:
        return self._expression

    def reset_scope(self, scope: gc_scope):
        "If scope has not been set, then we can set it"
        # TODO: #116 This feels like a kludge - should we pass around something else and get rid of this?
        if self._scope is None:
            self._scope = scope
        else:
            raise RuntimeError(
                "Internal Error: Scope is already set - it can't be set to a new value"
            )

    def scope(self) -> Union[gc_scope, gc_scope_top_level]:
        "Return the scope at which this variable becomes valid."
        if self._scope is not None:
            return self._scope
        else:
            raise RuntimeError(
                "Internal Error: Asking for the undefined scope of a value."
            )

    def cpp_type(self) -> ctyp.terminal:
        if self._cpp_type is None:
            raise RuntimeError(
                f"Internal Error: Variable {self._expression} does not have an assigned type, but needs one."
            )
        return self._cpp_type

    def has_cpp_type(self) -> bool:
        return self._cpp_type is not None

    def copy_with_new_scope(self, scope) -> cpp_value:
        "Make a new version, with just the scope changed"
        new_v = copy.copy(self)
        new_v._scope = scope
        return new_v

    def update_type(self, new_type: ctyp.terminal):
        """
        Update to a new type
        """
        self._cpp_type = new_type


class cpp_variable(cpp_value):
    r"""
    A value that can be declared. Refers to a variable.
    """

    def __init__(
        self,
        cpp_expression: str,
        scope: Union[gc_scope, gc_scope_top_level],
        cpp_type,
        initial_value: Optional[cpp_value] = None,
    ):
        cpp_value.__init__(self, cpp_expression, scope, cpp_type)
        self._initial_value = initial_value

    def initial_value(self):
        return self._initial_value

    def update_type(self, new_type: ctyp.terminal):
        if self._initial_value is not None:
            self._initial_value._cpp_type = new_type
        cpp_value.update_type(self, new_type)


class cpp_collection(cpp_value):
    r"""
    Represents a special kind of value - a collection (vector<float>).
    """

    def __init__(
        self,
        cpp_expression: str,
        scope: Union[gc_scope, gc_scope_top_level],
        collection_type: ctyp.collection,
    ):
        r"""
        Initialize a C++ value that can be turned into a sequence if requested.

        cpp_expression:         The expression in C++ to refer to this collection.
        scope:                  The scope at which this collection is valid.
        collection_type:        The type of the collection (see cpp_types). It should be a collection
        """
        cpp_value.__init__(self, cpp_expression, scope, collection_type)

    def get_element_type(self):
        "Return the type of the element of the sequence"
        return cast(ctyp.collection, self.cpp_type()).element_type

    def token_type(self):
        "Return the type of the token required, such as edm::EDGetTokenT<pat::MuonCollection> for miniAOD file"
        return None


class cpp_tuple(cpp_rep_base):
    r"""
    Represents a special kind of value - a tuple, which is just a container of other values. This
    isn't a regular cpp_value in the sense it can't be directly put into C++ code. It must be
    specially handled by the interpreter.
    """

    def __init__(
        self, list_of_values: tuple, scope: Union[gc_scope, gc_scope_top_level]
    ):
        """
        A Tuple holds a list of different types

        list_of_values:         Iterator that will give us all the cpp_xxx.
        scope:                  Scope where this is valid
        cpp_type:               An instance of cpp_types.tuple to specify the type.
        """
        cpp_rep_base.__init__(self)
        self._values = list_of_values
        self._scope = scope

    def values(self):
        return self._values

    def scope(self):
        return self._scope


class cpp_dict(cpp_rep_base):
    """Represents a special kind of value = a dict, which is just a keyed container of other values.
    This isn't a regular cpp_value in the sense it can't directly be put into C++ code. It must
    be specially handled by the interpreter.
    """

    def __init__(self, value: dict, scope: Union[gc_scope, gc_scope_top_level]):
        super().__init__()
        self._values = value
        self._scope = scope

    @property
    def value_dict(self) -> dict:
        return self._values

    def scope(self) -> Union[gc_scope, gc_scope_top_level]:
        return self._scope


class cpp_sequence(cpp_rep_base):
    """
    Represents an iterator over a sequence of data. The `sequence_value` points to value of the item in
    the stream, and `iterator_value` points to the iterator itself we are looping over (appears in the
    for statement).

    A sequence is a stream of values of a particular type. You can think of it like a generator expression,
    or like a iterator into a C++ vector of some type.
    """

    def __init__(
        self,
        sequence_value: Union[cpp_value, cpp_sequence],
        iterator_value: cpp_value,
        scope: Union[gc_scope_top_level, gc_scope],
        node: ast.expr,
    ):
        """
        Create a sequence

        sequence_value:         The value of the sequence - of the data items that are in sequence.
        iterator_value:         The iterator that is incremented to get the next value in the sequence. The
                                iterators scope is defined where it was created.
        scope:                  The scope at which this sequence is declared. Note that this may be different
                                from the of the iterator if we are, for example, inside an if statement caused
                                by a Where (or similar). In the case of the Where, the sequence scope will be
                                inside the if statement of the Where, while the iterator will be at the scope of
                                the original declaration. If the `sequence_value` is an actual value, it will have
                                the same scope.
        node:                   The AST node associated with this sequence.
        """
        cpp_rep_base.__init__(self)
        self._sequence = sequence_value
        self._iterator = iterator_value
        self._type: Optional[ctyp.collection] = None
        self._scope = scope
        self._node = node

    def sequence_value(self):
        return self._sequence

    def iterator_value(self):
        return self._iterator

    def cpp_type(self) -> ctyp.terminal:
        if self._type is None:
            self._type = ctyp.collection(self._sequence.cpp_type())
        return self._type

    def as_cpp(self):
        raise RuntimeError("Do not know how to get the cpp rep of a sequence!")

    def scope(self) -> Union[gc_scope, gc_scope_top_level]:
        "Return scope where this sequence was created/valid"
        return self._scope

    def node(self) -> ast.expr:
        "Node in ast tree where this sequence is defined."
        return self._node


def set_rep(node: ast.AST, value: cpp_rep_base, scope: Optional[Any] = None):
    """
    Set the representation of a node to a value.
    """
    node.rep = value  # type: ignore
    if scope is not None:
        node.scope = scope  # type: ignore


def get_rep(node: ast.AST) -> cpp_rep_base:
    """
    Get the representation of a node.
    """
    return node.rep  # type: ignore


# Allow dereference type for anything that is a value of some sort
DT = TypeVar("DT", bound=cpp_value)


def dereference_var(v: DT) -> DT:
    """
    If this is a pointer, return the object with the proper type (and a * to dereference it). Otherwise
    just return the object itself.

    NOTE: It might just return the object itself, not dereferencing it!
    """
    if not v.cpp_type().is_a_pointer:
        return v

    # We will go under the covers and "fix" this.
    new_v = copy.copy(v)
    new_v._expression = "*" + new_v._expression

    # There is only one type we current support here.
    # Eventually this is going to get us into trouble.
    new_v._cpp_type = new_v.cpp_type().get_dereferenced_type()
    return new_v


def base_type_member_access(v: cpp_value, extra_deref: int = 0) -> str:
    """
    Turn a C++ object into a base reference suitable for
    a member access.

    obj f => f.
    obj *f => f->
    obj **f => (*f)->

    v:            The object to access.
    extra_deref:  The number of extra dereferences to apply.
    """
    result = v.as_cpp()
    depth = extra_deref + v.cpp_type().p_depth
    for _ in range(1, depth):
        result = f"(*{result})"
    if depth > 0:
        return f"{result}->"
    else:
        return f"{result}."
