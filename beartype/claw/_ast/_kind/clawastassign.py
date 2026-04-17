#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **assignment statement abstract syntax tree (AST) transformer mixin**
(i.e., low-level superclass instrumenting assignment statements relevant to
runtime type-checking in modules hooked by :mod:`beartype.claw` import hooks).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from ast import (
    AST,
    AnnAssign,
    Assign,
    Attribute,
    Call,
    Name,
    unparse,
)
from beartype._data.claw.dataclawmagic import BEARTYPE_RAISER_FUNC_NAME
from beartype._conf.confcommon import BEARTYPE_CONF_DEFAULT
from beartype._data.typing.datatyping import NodeVisitResult
from beartype._util.ast.utilastmake import (
    make_node_call_expr,
    make_node_kwarg,
    make_node_name_load,
    make_node_object_attr_load,
    make_node_str,
)
from beartype._util.text.utiltextansi import color_attr_name

# ....................{ SUBCLASSES                         }....................
class BeartypeNodeTransformerAssignMixin(object):
    '''
    Beartype :pep:`526`-compliant **abstract syntax tree (AST) node
    transformer** (i.e., visitor pattern recursively transforming *all*
    :pep:`526`-compliant annotated variable assignments in the AST tree passed
    to the :meth:`visit` method of the
    :class:`beartype.claw._ast.clawastmain.BeartypeNodeTransformer` subclass
    also subclassing this mixin).
    '''

    # ..................{ VISITORS ~ pep : 526               }..................
    def visit_Assign(self, node: Assign) -> NodeVisitResult:
        '''
        Track the passed **assignment node** (i.e., node signifying the
        assignment of an attribute) if this node signifies an instantiation of a
        third-party type defining one or more decorator-hostile decorators
        previously imported into a scope of the currently visited module.

        Parameters
        ----------
        node : Assign
            Assignment node to be tracked.

        Returns
        -------
        NodeVisitResult
            This assignment node unmodified.
        '''
        pass

    # ..................{ VISITORS ~ pep : 526               }..................
    def visit_AnnAssign(self, node: AnnAssign) -> NodeVisitResult:
        '''
        Add a new child node to the passed **annotated assignment node** (i.e.,
        node signifying the assignment of an attribute annotated by a
        :pep:`526`-compliant type hint) inserting a subsequent statement
        following that annotated assignment type-checking that attribute against
        that type hint by passing both to our :func:`beartype.door.is_bearable`
        tester.

        This visitor also additionally track this node if this node signifies an
        instantiation of a third-party type defining one or more
        decorator-hostile decorators previously imported into a scope of the
        currently visited module.

        Design
        ------
        Note that the :class:`.AnnAssign` subclass defines these instance
        variables:

        * ``node.annotation``, a child node describing the PEP-compliant type
          hint annotating this assignment, typically an instance of either:

          * :class:`ast.Name`.
          * :class:`ast.Constant`.

          Note that this node is *not* itself a valid PEP-compliant type hint
          and should *not* be treated as such here or elsewhere.
        * ``node.target``, a child node describing the target attribute assigned
          to by this assignment, guaranteed to be an instance of either:

          * :class:`ast.Name`, in which case this is a **simple assignment**
            (i.e., to a local or global variable). This is the common case in
            which the attribute being assigned to is *NOT* embedded in
            parentheses and thus denotes a simple attribute name rather than a
            full-blown Python expression.
          * :class:`ast.Attribute`, in which case this is an **object
            assignment** (i.e., to an instance or class variable of an object).
          * :class:`ast.Subscript`, in which case this assignment is to the item
            subscripted by an index of a container rather than to that container
            itself.

        * ``node.simple``, an integer :superscript:`sigh` that is either:

          * If ``node.target`` is an :class:`ast.Name` node, 1.
          * Else, 0.

        * ``node.value``, an optional child node defined as either:

          * If this attribute is actually assigned to, a node encapsulating
            the new value assigned to this target attribute.
          * Else, :data:`None`.

        Caveats
        -------
        You may now be thinking to yourself as you wear a bear hat while
        rummaging through this filthy code: "What do you mean, 'if this
        attribute is actually assigned to'? Isn't this attribute necessarily
        assigned to? Isn't that what the 'AnnAssign' subclass means? I mean,
        it's right there in the bloody subclass name: 'AnnAssign', right?
        Clearly, *something* is bloody well being assigned to. Right?"
        Wrong. The name of the :class:`.AnnAssign` subclass was poorly chosen.
        That subclass ambiguously encapsulates both:

        * Annotated variable assignments (e.g., ``muh_attr: int = 42``).
        * Annotated variables *without* assignments (e.g., ``muh_attr: int``).

        Parameters
        ----------
        node : AnnAssign
            Annotated assignment node to be transformed.

        Returns
        -------
        NodeVisitResult
            Either:

            * If this annotated assignment node is *not* **simple** (i.e., the
              attribute being assigned to is embedded in parentheses and thus
              denotes a full-blown Python expression rather than a simple
              attribute name), that same parent node unmodified.
            * If this annotated assignment node is *not* **assigned** (i.e., the
              attribute in question is simply annotated with a type hint rather
              than both annotated with a type hint *and* assigned to), that same
              parent node unmodified.
            * Else, a 2-list comprising both that node and a new adjacent
              :class:`Call` node performing this type-check.

        See Also
        --------
        https://github.com/awf/awfutils
            Third-party Python package whose ``@awfutils.typecheck`` decorator
            implements statement-level :func:`isinstance`-based type-checking in
            a similar manner, strongly inspiring this implementation. Thanks so
            much to Cambridge researcher @awf (Andrew Fitzgibbon) for the
            phenomenal inspiration!
        '''
        pass
