from __future__ import annotations

import copy
from dataclasses import dataclass
import logging
from typing import Dict, List, Optional, Union


@dataclass
class CPPParsedTypeInfo:
    """
    A parsed type, with the type and whether it's a pointer.
    """

    # The type name (`int`, `vector<float`, etc.)
    name: str

    # Pointer, and how many (2 for `int**`, 0 for `int`, etc.)
    pointer_depth: int

    # True if this is a const variable
    is_const: bool = False

    def __str__(self):
        return self.name + "*" * self.pointer_depth


def parse_type(t_name: str) -> CPPParsedTypeInfo:
    """Convert a type name string into info for a type

    Args:
        t_name (str): The type name (`float`, `float*`)

    Returns:
        CPPParsedTypeInfo: Parsed info from the type
    """
    ptr_depth = 0
    while True:
        t_name = t_name.strip()
        if t_name.endswith("*"):
            ptr_depth += 1
            t_name = t_name[:-1]
        else:
            break

    if t_name.startswith("const "):
        is_const = True
        t_name = t_name[6:]
    else:
        is_const = False

    return CPPParsedTypeInfo(t_name, ptr_depth, is_const)


class terminal:
    "Represents something we cannot see inside, like float, or int, or bool"

    def __init__(
        self,
        t: Union[str, CPPParsedTypeInfo],
        p_depth: int = 0,
        is_const: bool = False,
        tree_type: Optional[str] = None,
    ):
        """Create a terminal type - a type that we do not need to see inside

        * int
        * float
        * MyOwnStruct

        Use `p_depth` to represent how indirect to get down to the type (int* is 1, for
        example).)

        Args:
            t (str|CPPParsedTypeInfo): The type to represent
            p_depth (int): How many levels of indirection to get to the type
            is_const (bool): Whether this is a const type
            tree_type (str): Type to send back as a leaf.
        """
        if isinstance(t, CPPParsedTypeInfo):
            self._type = t.name
            self._p_depth = t.pointer_depth
            self._is_const = t.is_const
        else:
            self._type = t
            self._p_depth = p_depth
            self._is_const = is_const
        self._tree_type = tree_type

    def __str__(self):
        c_str = "const " if self.is_const else ""
        return f"{c_str}{self.type}{'*' * self._p_depth}"

    @property
    def is_a_pointer(self) -> bool:
        "Returns true if this terminal is a pointer"
        return self._p_depth > 0

    @property
    def p_depth(self) -> int:
        "Return how many levels of indirection to get to the type"
        return self._p_depth

    @property
    def is_const(self) -> bool:
        "Returns true if this terminal is a const type"
        return self._is_const

    def default_value(self):
        raise NotImplementedError()

    @property
    def type(self) -> str:
        return self._type

    @property
    def tree_type(self) -> terminal:
        return (
            self
            if self._tree_type is None
            else terminal(
                self._tree_type, p_depth=self._p_depth, is_const=self._is_const
            )
        )

    def get_dereferenced_type(self) -> terminal:
        "Type after dereferencing it once. Will throw if this type cannot be dereferenced"
        if self._p_depth == 0:
            raise RuntimeError(f"Cannot dereference type {self}")

        # Do deep copy because this needs to work in subclasses.
        new_t = copy.copy(self)
        new_t._p_depth -= 1
        return new_t


class terminal_enum_value(terminal):
    def __init__(self, en_info: ENumInfo):
        """Create a terminal that is an enum value.

        Args:
            t (str): The enum value as a type
        """
        super().__init__(str(en_info))


class collection(terminal):
    "Represents a collection/list/vector of the same type"

    def __init__(
        self,
        element_type: terminal,
        array_type: Optional[Union[str, CPPParsedTypeInfo]] = None,
        p_depth: int = 0,
    ):
        """Create a collection type, like `vector<float>`.

        Args:
            element_type (terminal): The element type, like a `terminal` of `float`.
            array_type (Optional[Union[str, CPPParsedTypeInfo]], optional): The type of the array. Defaults to None. Everything
                    is lifted from `array_type` if it is a `CPPParsedTypeInfo`.
            p_depth (int, optional): If the array type is a pointer or not. Defaults to 0. Ignored if `array_type` is `CPPParsedTypeInfo`.
        """
        if array_type is None:
            super().__init__(f"std::vector<{element_type}>", p_depth=p_depth)
        elif isinstance(array_type, CPPParsedTypeInfo):
            super().__init__(array_type)
        else:
            super().__init__(array_type, p_depth=p_depth)

        # And the element type we are representing
        self._element_type = element_type

    def token_type(self):
        # Return the type of the token. This token can be used to get data via
        # functions like getByToken()
        return None

    # TODO: Turn into a property
    @property
    def element_type(self) -> terminal:
        "The type of element that this collection holds"
        return self._element_type


###########################
# Manage types


@dataclass
class MethodInvokeInfo:
    "Method invocation info"

    # The return type
    r_type: terminal

    # Number of dereferences to apply to the calling object. Normally zero.
    # 0: obj.method()
    # 1: obj->method(), etc.
    deref_depth: int


g_method_type_dict: Dict[str, Dict[str, MethodInvokeInfo]] = {}


def add_method_type_info(
    type_string: str, method_name: str, t: terminal, deref_depth: int = 0
):
    """
    Define a return type for a method

    type_string         String of the object the method is calling against
    method_name         Name of the object
    t                   The type (terminal, collection, etc.) of return type
    """
    if type_string not in g_method_type_dict:
        g_method_type_dict[type_string] = {}
    g_method_type_dict[type_string][method_name] = MethodInvokeInfo(t, deref_depth)


def method_type_info(type_string: str, method_name: str) -> Optional[MethodInvokeInfo]:
    """
    Return the type of the method's return value
    """
    if type_string not in g_method_type_dict:
        return None
    if method_name not in g_method_type_dict[type_string]:
        return None
    return g_method_type_dict[type_string][method_name]


@dataclass
class ENumInfo:
    "Information about an enum"

    # The name of the enum
    name: str

    # List of the value names it can take on
    values: List[str]

    # The namespace we are hosted in
    ns: NameSpaceInfo

    # The full name
    @property
    def full_name(self) -> str:
        return f"{self.ns.full_name}.{self.name}"

    def __str__(self) -> str:
        return self.full_name

    def value_as_cpp(self, value: str) -> str:
        """Returns the C++ string for this value. It is assumed value
        is part of our value list.

        Args:
            value (str): The value we should use.

        Returns:
            str: The C++ specification for the type.
        """
        return f"{self.ns.full_name}::{value}".replace(".", "::")


class NameSpaceInfo:
    "Information about a namespace"

    def __init__(self, name, hosting_ns: Optional[NameSpaceInfo]):
        self.ns_name = name
        self.names_spaces = {}
        self.enums = {}
        self.parent_ns = hosting_ns

    ns_name: str

    names_spaces: Dict[str, NameSpaceInfo]

    enums: Dict[str, ENumInfo]

    parent_ns: Optional[NameSpaceInfo] = None

    @property
    def full_name(self) -> str:
        "The full name of the namespace"
        return (
            f"{self.parent_ns.full_name}.{self.ns_name}"
            if self.parent_ns is not None
            else self.ns_name
        )

    def get_ns(self, ns_name: str) -> Optional[NameSpaceInfo]:
        "Return the namespace with the given name, or None if it does not exist"
        return self.names_spaces.get(ns_name, None)

    def get_enum(self, enum_name: str) -> Optional[ENumInfo]:
        "Return the enum with the given name, or None if it does not exist"
        return self.enums.get(enum_name, None)

    def __str__(self) -> str:
        return self.full_name


# The top level namespaces we know about
g_toplevel_ns: Dict[str, NameSpaceInfo] = {}


def get_toplevel_ns(ns_name: str) -> Optional[NameSpaceInfo]:
    """
    Return the AST for a top level namespace. This is used to resolve
    the type of a method call.
    """
    return g_toplevel_ns.get(ns_name, None)


def define_ns(ns_name: str) -> NameSpaceInfo:
    """Define a namespace.

    `ns_name` can be in the form:
        - `bogus` - defines a single level namespace
        - 'bogus.sub' - creates we `NameSpaceInfo` objects, placing the one for
          `sub` inside the one for `bogus`, which is places in the global ns dict.

    If the namespace is already defined, this function will return the existing
    namespace.

    Args:
        ns_name (str): Name of the namespace to define

    Returns:
        NameSpaceInfo: The defined namespace.
    """
    parts = ns_name.split(".")
    v = g_toplevel_ns.get(parts[0], None)
    if v is None:
        v = NameSpaceInfo(parts[0], None)
        g_toplevel_ns[parts[0]] = v
    for p in parts[1:]:
        w = v.get_ns(p)
        if w is None:
            w = NameSpaceInfo(p, v)
            v.names_spaces[p] = w
        v = w
    return v


def define_enum(ns_name: str, enum_name: str, enum_values: List[str]) -> ENumInfo:
    """Define a new enum.

    The enum is defined in the `ns_name` namespace, with the name `enum_name` and
    `enum_values`. The newly created `ENumInfo` object is returned.

    It is an error to try to create the same `enum` twice.

    Args:
        ns_name (str): The name of the namespace (can contain `.`)
        enum_name (str): The name of the enum
        enum_values (List[str]): The list of names the enum is allowed.

    Returns:
        ENumInfo: _description_
    """
    ns = define_ns(ns_name)
    if enum_name in ns.enums:
        logging.getLogger(__name__).info(
            f"Enum {enum_name} already defined in namespace {ns_name}"
        )
        return ns.enums[enum_name]

    e = ENumInfo(enum_name, enum_values, ns)
    ns.enums[enum_name] = e

    return e
