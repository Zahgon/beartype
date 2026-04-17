#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **import statement abstract syntax tree (AST) transformer mixin**
(i.e., low-level superclass instrumenting import statements relevant to runtime
type-checking in modules hooked by :mod:`beartype.claw` import hooks).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ TODO                               }....................
#FIXME: Unit test the newly defined
#"BeartypeDecorPlace.LAST_BEFORE_DECOR_HOSTILE" position, please.

#FIXME: Handle user-defined beforelists via the "self._conf" instance
#variable, please. *sigh*

# ....................{ IMPORTS                            }....................
from ast import (
    AST,
    Call,
    ClassDef,
    Import,
    ImportFrom,
    Name,
    alias,
    expr,
    unparse,
)
from beartype.claw._ast._scope.clawastscope import BeartypeNodeScope
from beartype.roar import (
    BeartypeClawAstImportException,
    BeartypeClawImportConfException,
)
from beartype.typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)
from beartype._cave._cavemap import NoneTypeOr
from beartype._conf.confmain import BeartypeConf
from beartype._conf.confcommon import BEARTYPE_CONF_DEFAULT
from beartype._conf.decorplace.confplaceenum import BeartypeDecorPlace
from beartype._conf.decorplace.confplacetrie import (
    BeartypeDecorPlaceTrieABC,
    BeartypeDecorPlaceInstanceTrie,
    BeartypeDecorPlaceTypeTrie,
)
from beartype._data.api.standard.dataast import NODE_CONTEXT_LOAD
from beartype._data.conf.dataconfplace import BeartypeDecorPlaceSubtrie
from beartype._data.claw.dataclawmagic import BEARTYPE_DECORATOR_FUNC_NAME
from beartype._data.kind.datakindiota import (
    SENTINEL,
    Iota,
)
# from beartype._data.kind.datakindmap import FROZENDICT_EMPTY
from beartype._data.typing.datatyping import (
    ListStrs,
    NodeDecoratable,
    NodeVisitResult,
)
from beartype._util.ast.utilastget import (
    get_node_attr_basenames,
    get_node_attr_basename_first,
    get_node_repr_indented,
)
from beartype._util.ast.utilastmunge import copy_node_metadata
# from beartype._util.kind.maplike.utilmapfrozen import FrozenDict
from beartype._util.module.pep.modpep328 import (
    canonicalize_pep328_module_name_relative)

# ....................{ SUBCLASSES                         }....................
class BeartypeNodeTransformerImportMixin(object):
    '''
    Beartype **decorator-hostile tracker** (i.e., visitor pattern recursively
    tracking imports of third-party decorator-hostile decorators as well as the
    modules and types defining such decorators across *all* import statements in
    the AST tree passed to the :meth:`visit` method of the
    :class:`beartype.claw._ast.clawastmain.BeartypeNodeTransformer` subclass
    also subclassing this mixin).

    This tracker manages the **beartype decorator beforelist** (i.e., collection
    of data structures deciding where the :func:`beartype.beartype` decorator
    should be applied in chains of one or more third-party decorators decorating
    callables and types). This tracker detects third-party decorators well-known
    to be **decorator-hostile** (i.e., decorators hostile to other decorators by
    prematurely terminating decorator chaining such that *no* decorators may
    appear above those decorators in any chain of one or more decorators).

    Attributes
    ----------
    _attr_basenames : Optional[list[str]]
        List of the one or more unqualified basenames comprising the possibly
        fully-qualified name of the current attribute being inspected (e.g.,
        decorator visited by iteration internally performed in the
        :def:`_decorate_node_beartype` method), enabling that inspection to
        reconstruct that name. Specifically, this is either:

        * If the low-level :func:`.get_node_attr_basenames` getter has yet to be
          called by a method of this mixin, :data:`None`.
        * Else, this list.
        '''

    # ..................{ CLASS VARIABLES                    }..................
    # Squelch false negatives from mypy. This is absurd. This is mypy.
    if TYPE_CHECKING:
        _scope: BeartypeNodeScope

    # ..................{ INITIALIZERS                       }..................
    def __init__(self) -> None:
        '''
        Initialize this node transformer mixin.
        '''

        # Initialize our superclass.
        super().__init__()

        # Nullify all instance variables for safety.
        self._attr_basenames: Optional[ListStrs] = None

    # ..................{ MAPPERS                            }..................
    def map_node_attr_imported_to_assigned(
        self, node_name_imported: AST, node_name_assigned: AST) -> None:
        '''
        Map the source attribute (whose possibly fully-qualified name is
        encapsulated by the passed node) previously imported into the current
        lexical scope of the currently visited module to the target attribute
        (whose possibly fully-qualified name is encapsulated by the passed node)
        assigned in this same scope if this source attribute is a third-party
        type transitively defining decorator-hostile decorators *or* silently
        reduce to a noop otherwise (i.e., if this source attribute is *not* such
        a type).

        This public method is intended to be called by external ``visit_*``
        methods of sibling mixins of the
        :class:`beartype.claw._ast.clawastmain.BeartypeNodeTransformer` class.
        Sibling mixins call this method to notify this decorator-hostile tracker
        of an instantiation of a third-party type known to define
        decorator-hostile decorator methods.

        Parameters
        ----------
        node_name_imported : AST
            Node possibly encapsulating the fully-qualified name or unqualified
            basename of a source type in an assignment statement.
        node_name_assigned : AST
            Node possibly encapsulating the fully-qualified name or unqualified
            basename of a target instance of that type in an assignment
            statement.
        '''
        pass

    # ..................{ VISITORS                           }..................
    def visit_Import(self, node: Import) -> NodeVisitResult:
        '''
        Track the passed **import node** (i.e., node signifying the importation
        of a module or package) if this node signifies an import of a module or
        package defining one or more decorator-hostile decorators.

        Parameters
        ----------
        node : Import
            Possibly problematic import node to be tracked.

        Returns
        -------
        NodeVisitResult
            The passed import node unmodified.
        '''
        pass


    def visit_ImportFrom(self, node: ImportFrom) -> NodeVisitResult:
        '''
        Track the passed **import-from node** (i.e., node signifying the
        importation of an attribute from a module or package) if this node
        signifies an import of either:

        * A decorator-hostile decorator.
        * A module defining one or more decorator-hostile decorators.
        * A type defining one or more decorator-hostile decorators.

        Parameters
        ----------
        node : ImportFrom
            Possibly problematic import-from node to be tracked.

        Returns
        -------
        NodeVisitResult
            The passed import-from node unmodified.
        '''
        pass

    # ....................{ PRIVATE ~ mappers              }....................
    def _map_scoped_attr_name_to_subtrie(
        self,
        attr_name: str,
        attr_name_subtrie: Optional[BeartypeDecorPlaceSubtrie],
    ) -> None:
        '''
        Map the passed possibly fully-qualified name of a third-party
        decorator-hostile attribute accessible to this scope (e.g., by an import
        or assignment statement) to the passed **scoped attribute name subtrie**
        (i.e., recursive tree structure whose nodes are the unqualified
        basenames of third-party attributes imported into a scope of the
        currently visited module such that these attributes are either
        themselves decorator-hostile decorators *or* submodules, types, or
        instances transitively defining decorator-hostile decorators).

        Parameters
        ----------
        attr_name : str
            Possibly fully-qualified name of the attribute to be mapped.
        attr_name_subtrie : Optional[BeartypeDecorPlaceSubtrie]
            Either:

            * If this attribute is a decorator-hostile decorator, :data:`None`.
            * If this attribute is a submodule, type, or instance transitively
              defining one or more decorator-hostile decorators, the attribute
              name subtrie to map this attribute name to.
        '''
        pass

    # ....................{ PRIVATE ~ decorators           }....................
    #FIXME: Revise docstring, please. This method now employs a highly
    #non-trivial algorithm to decide the correct @beartype decorator position in
    #a chain of one or more existing non-@beartype decorators.
    #FIXME: Unit test us up, please.
    def _decorate_node_beartype(
        self, node: NodeDecoratable, conf: BeartypeConf) -> None:
        '''
        Add a new **child beartype decoration node** (i.e., abstract syntax tree
        (AST) node applying the :func:`beartype.beartype` decorator configured
        by the passed beartype configuration) to the passed **parent decoratable
        node** (i.e., AST node encapsulating the definition of a pure-Python
        object supporting decoration by one or more ``"@"``-prefixed
        decorations, including both pure-Python classes *and* callables).

        Note that this function **prepends** rather than appends this child
        decoration node to the beginning of the list of all child decoration
        nodes for this parent decoratable node. Since that list is "stored
        outermost first (i.e. the first in the list will be applied last)",
        prepending guarantees that the beartype decorator will be applied last
        (i.e., *after* all other decorators). This ensures that explicitly
        configured beartype decorations applied to this decoratable by the end
        user (e.g., ``@beartype(conf=BeartypeConf(...))``) assume precedence
        over implicitly configured beartype decorations applied by this
        function.

        Parameters
        ----------
        node : AST
            **Decoratable node** (i.e., parent class or callable node) to add a
            new child beartype decoration node to.
        conf : BeartypeConf
            **Beartype configuration** (i.e., dataclass configuring the
            :mod:`beartype.beartype` decorator for some decoratable object(s)
            decorated by a parent node passing this dataclass to that
            decorator).
        '''
        pass


    def _decorate_node_beartype_last_before_decor_hostile(
        self,
        node: NodeDecoratable,
        conf: BeartypeConf,
        node_beartype_decorator: expr,
    ) -> None:
        '''
        Add a new child :func:`beartype.beartype` decoration node to the passed
        parent decoratable node subject to
        :attr:`BeartypeDecorPlace.LAST_BEFORE_DECOR_HOSTILE` positioning.

        This method contextually injects the :func:`beartype.beartype` decorator
        as high (i.e., late) in the chain of decorators decorating the type
        or callable encapsulated by this parent decoratable node as feasible
        while still preserving compatibility with decorator-hostile decorators.
        To do so, this method injects this decorator immediately *before* the
        lowest (i.e., earliest) decorator-hostile decorator decorating this type
        or callable as externally configured by the beforelist and previously
        detected by the ``visit_Import*()`` family of methods defined above.

        Parameters
        ----------
        node : AST
            **Decoratable node** (i.e., parent type or callable node) to add a
            new child beartype decoration node to.
        conf : BeartypeConf
            **Beartype configuration** (i.e., dataclass configuring the
            :mod:`beartype.beartype` decorator for some decoratable object(s)
            decorated by a parent node passing this dataclass to that
            decorator).
        node_beartype_decorator : expr
            Child decoration node decorating this parent type or callable node
            by the :func:`beartype.beartype` decorator.
        '''
        pass
        # print(f'Decorator list after @beartype injection: {unparse(node.decorator_list)}')

    # ....................{ PRIVATE ~ finders              }....................
    def _is_node_scoped_attr_name(self, node: AST) -> Union[
        BeartypeDecorPlaceSubtrie, bool]:
        '''
        :data:`True` if the attribute name (presumably referenced from the
        current scope of the currently visited module) encapsulated by the
        passed node is that of a previously imported decorator-hostile
        decorator, an **imported decorator-hostile attribute name subtrie**
        (i.e., recursive tree structure whose nodes are the unqualified
        basenames of third-party attributes imported into a scope of the
        currently visited module such that these attributes are either
        themselves decorator-hostile decorators *or* submodules, types, or
        instances transitively defining decorator-hostile decorators) if that
        attribute name is that of a previously imported submodule, type, or
        instance transitively defining one or more decorator-hostile decorators,
        or :data:`False` otherwise (i.e., if this attribute name is *not* that
        of either a previously imported decorator-hostile decorator *or* a
        submodule, type, or instance transitively defining such decorators).

        This finder identifies whether the passed attribute name refers to a
        previously imported decorator-hostile decorator or not. Specifically,
        this finder (in order):

        #. Splits the possibly fully-qualified attribute name encapsulated by
           this attribute name node on ``"."`` delimiters into its constituent
           unqualified basenames.
        #. For each such unqualified basename:

           * If there exists a child subtrie of the current parent imported
             decorator-hostile attribute name (sub)trie (starting at the root
             decorator-hostile attribute name trie) whose associated key is
             this basename:

             * If that child subtrie is :data:`None` (signifying that child
               subtrie to be a terminal leaf node and thus a decorator-hostile
               decorator function or method), return :data:`True`.
             * Else, recurse into that subtrie.

           * Else, return either:

             * If this is the first unqualified basename and no such child
               subtrie exists, :data:`False`.
             * Else, that child subtrie.

        Parameters
        ----------
        node : AST
            Node possibly encapsulating the name of an attribute referenced from
            some scope of the currently visited module.

        Returns
        -------
        Optional[Union[BeartypeDecorPlaceSubtrie, Iota]]
            Either:

            * If this attribute name refers to a previously imported
              decorator-hostile decorator, :data:`True`.
            * If this attribute name refers to a previously imported submodule,
              type, or instance transitively defining one or more
              decorator-hostile decorators, the imported decorator-hostile
              attribute name subtrie describing the contents of that submodule,
              type, or instance.
            * Else (i.e., if this attribute name refers to neither a previously
              imported decorator-hostile decorator *nor* a submodule, type, or
              instance transitively defining these decorators),
              :data:`False`.
        '''
        pass
