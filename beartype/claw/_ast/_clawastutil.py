#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **abstract syntax tree (AST) mungers** (i.e., low-level callables
modifying various properties of various nodes in the currently visited AST).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from ast import (
    AST,
    Call,
    ClassDef,
    Name,
    Subscript,
    expr,
    keyword,
)
from beartype._data.api.standard.dataast import NODE_CONTEXT_LOAD
from beartype._data.claw.dataclawmagic import BEARTYPE_CLAW_STATE_OBJ_NAME
from beartype._util.ast.utilastmake import (
    make_node_kwarg,
    make_node_object_attr_load,
    make_node_str,
)
from beartype._util.ast.utilastmunge import copy_node_metadata

# ....................{ SUBCLASSES                         }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAUTION: To improve forward compatibility with the superclass API over which
# we have *NO* control, avoid accidental conflicts by suffixing *ALL* private
# and public attributes of this subclass by "_beartype".
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class BeartypeNodeTransformerUtilityMixin(object):
    '''
    **Beartype abstract syntax tree (AST) node utility transformer** (i.e.,
    low-level mixin of the high-level
    :class:`beartype.claw._ast.clawastmain.BeartypeNodeTransformer` subclass
    supplementing that subclass with various low-level methods creating,
    modifying, and introspecting common node types and subclass properties).
    '''

    # ....................{ PRIVATE ~ factories            }....................
    #FIXME: Unit test us up, please.
    def _make_node_keyword_conf(self, node_sibling: AST) -> keyword:
        '''
        Create and return a new **beartype configuration keyword argument node**
        (i.e., abstract syntax tree (AST) node passing the beartype
        configuration associated with the currently visited module as a ``conf``
        keyword to a :func:`beartype.beartype` decorator orchestrated by the
        caller).

        Parameters
        ----------
        node_sibling : AST
            Sibling node to copy source code metadata from.

        Returns
        -------
        keyword
            Keyword node passing this configuration to an arbitrary function.
        '''
        pass
