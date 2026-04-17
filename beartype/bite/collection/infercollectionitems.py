#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype Inferential Type-hint Engine (BITE) collection items type hint
inferrers** (i.e., lower-level functions dynamically inferring subscripted type
hints describing pure-Python containers containing one or more items).
'''

# ....................{ IMPORTS                            }....................
from beartype.roar import BeartypeConfException
from beartype.typing import (
    Counter,
    Optional,
    Tuple,
)
from beartype._conf.confmain import BeartypeConf
from beartype._conf.confenum import BeartypeStrategy
from beartype._data.typing.datatyping import FrozenSetInts
from beartype._util.hint.pep.proposal.pep646.pep484585646tuple import (
    make_hint_pep484585_tuple_fixed)
from beartype._util.hint.pep.proposal.pep484.pep484604union import (
    make_hint_pep484604_union)
from beartype._util.kind.integer.utilintget import (
    get_integer_pseudorandom_signed_32bit)
from collections.abc import (
    Collection as CollectionABC,
    Mapping as MappingABC,
    Sequence as SequenceABC,
)

# ....................{ INFERERS                           }....................
def infer_hint_collection_items(
    # Mandatory parameters.
    obj: CollectionABC,
    hint_factory: object,
    conf: BeartypeConf,
    __beartype_obj_ids_seen__: FrozenSetInts,

    # Optional parameters.
    origin_type: Optional[type] = None,
) -> object:
    '''
    Type hint recursively validating the passed collection (including *all*
    items transitively reachable from this collection), defined by subscripting
    the passed type hint factory by the union of the child type hints validating
    these items.

    This function *cannot* be memoized, due to necessarily accepting the
    ``__beartype_obj_ids_seen__`` parameter unique to each call to the parent
    :func:`beartype.bite.infer_hint` function.

    Parameters
    ----------
    obj : CollectionABC
        Collection to infer a type hint from.
    hint_factory : object
        Subscriptable type hint factory validating this collection (e.g., the
        :pep:`585`-compliant :class:`list` builtin type if this collection is a
        list).
    conf : BeartypeConf, optional
        **Beartype configuration** (i.e., self-caching dataclass encapsulating
        all settings configuring type-checking for the passed object).
    __beartype_obj_ids_seen__ : FrozenSet[int]
        **Recursion guard.** See also the parameter of the same name accepted by
        the :func:`beartype.bite.inferhint.infer_hint` function.
    origin_type : Optional[type]
        Either:

        * If the caller requires support for so-called "virtual subclasses" in
          which the passed ``obj`` collection is an instance of a user-defined
          class that does *not* explicitly subclass a :mod:`collections.abc`
          abstract base class (ABC) but does nonetheless implicitly satisfy the
          protocol implied by such an ABC, the ABC implicitly satisfied by this
          collection. Ideally, all :mod:`collections.abc` collections would
          support virtual subclassing by defining the ``__subclasshook__()`
          dunder method. Indeed, most do -- but some (e.g.,
          :class:`collections.abc.Mapping`) do *not*. This parameter enables
          callers to overcome this probably unintentional oversight in CPython.
        * Else, :data:`None`. In this case, this parameter actually defaults to
          the type of the passed ``obj`` collection.

        Defaults to :data:`None`.

    Returns
    -------
    object
        Type hint inferred from the passed collection.

    Warns
    -----
    BeartypeDoorInferHintRecursionWarning
        On detecting that the passed iterable is **recursive** (i.e.,
        containing one or more items that self-referentially refer to this same
        iterable).
    '''
    assert isinstance(obj, CollectionABC), f'{repr(obj)} not collection.'
    assert isinstance(conf, BeartypeConf), f'{repr(conf)} not configuration.'
    assert isinstance(__beartype_obj_ids_seen__, frozenset), (
        f'{repr(__beartype_obj_ids_seen__)} not frozen set.')

    # ....................{ PREAMBLE                       }....................
    # If this collection is empty, return the this unsubscripted hint factory
    # permissively matching *ALL* collections of this type. Since *NO* child
    # type hints can be safely inferred from an empty collection, our only
    # recourse is to allow similar instances of this collection to contain *ALL*
    # possible items.
    if not obj:
        return hint_factory
    # Else, this collection is non-empty.
    #
    # If no origin type was passed, default this to the type of this collection.
    elif origin_type is None:
        origin_type = obj.__class__
    # Else, an origin type was passed. Preserve this type as is.
    assert isinstance(origin_type, type), (
        f'{repr(origin_type)} not type.')

    # ....................{ LOCALS                         }....................
    # Add the integer uniquely identifying this collection to this set, thus
    # recording that this collection has now been visited by this recursion.
    __beartype_obj_ids_seen__ |= {id(obj)}

    # Low-level private callable defined below suitable for inferring the full
    # type hint recursively validating this collection, defined as either...
    hint_inferer = (
        # If this collection is a mapping, the mapping-specific inferer;
        #
        # Ideally, detecting whether a collection is a mapping would be
        # trivially feasible with a standard one-liner resembling:
        #     if isinstance(obj, collections.abc.Mapping) else
        #
        # Unfortunately, the "collections.abc.Mapping" ABC is *BROKEN.* Unlike
        # most other "collections.abc" superclasses, "Mapping" fails to define
        # the __subclasshook__() dunder method and thus fails to support the
        # so-called "virtual subclasses" that most "collections.abc"
        # superclasses support. See also this relevant StackOverflow answer:
        #     https://stackoverflow.com/a/64666157/2809027
        #
        # Our only recourse is to require that callers requiring support for
        # "virtual subclasses" pass a distinct "hint_origin_type" class that
        # can then be tested as a "collections.abc.Mapping" subclass.
        _infer_hint_mapping_items
        if issubclass(origin_type, MappingABC) else
        # Else, this collection is *NOT* a mapping. In this case, the
        # general-purpose inferer applicable to *ALL* single-argument
        # reiterables (e.g., collections whose type hint factories are
        # subscriptable by only a single child type hint).
        _infer_hint_reiterable_items
    )
    # print(f'Inferring {repr(obj)} child hints with {repr(hint_inferer)}...')

    # Type hint recursively validating this collection.
    hint = hint_inferer(
        obj=obj,  # type: ignore[arg-type]
        hint_factory=hint_factory,
        conf=conf,
        __beartype_obj_ids_seen__=__beartype_obj_ids_seen__,
    )

    # Return this hint.
    return hint

# ....................{ PRIVATE ~ constants                }....................
_ROOT_TUPLE_FIXED_ITEMS_LEN_MAX = 10
'''
Maximum inclusive number of tuple items below which the private
:func:`._infer_hint_reiterable_items` function infers a **root tuple** (i.e.,
top-most object originally passed by the caller to the public
:func:`beartype.bite.infer_hint` function) to be validated by a **fixed-length
tuple type hint** of the form ``tuple[{hint_child1}, ???, {hint_childN}]``.

Specifically, for each root tuple containing:

* Less than or equal to this number of items, this tuple is annotated by a
  **fixed-length tuple type hint** of the form ``tuple[{hint_child1}, ???,
  {hint_childN}]``.
* Greater than this number of items, this tuple is annotated by a **variadic
  tuple type hint** of the form ``tuple[{hint_childs}, ...]``.

This magic number enables an ad-hoc heuristic for disambiguating between
fixed-length and variadic tuple type hints. Technically, *any* tuple may be
ambiguously annotated as either. Pragmatically, fixed-length tuple type hints
exist almost exclusively to annotate **multiple-return functions** (i.e.,
functions returning two or more values as a tuple whose items are those values);
variadic tuple type hints annotate all other tuples, which is most of them.
Since all multiple-return functions return a root tuple *and* since most
real-world multiple-return functions of interest return a root tuple containing
less than or equal to this magic number of items, this heuristic follows.
'''

# ....................{ PRIVATE ~ inferers                 }....................
def _infer_hint_mapping_items(
    obj: MappingABC,
    hint_factory: object,
    conf: BeartypeConf,
    __beartype_obj_ids_seen__: FrozenSetInts,
) -> object:
    '''
    Type hint recursively validating the passed **mapping** (i.e.,
    collections whose type hint factories are subscriptable by a pair of child
    key and value type hints) and all keys *and* values transitively reachable
    from this mapping, defined by subscripting the passed type hint factory by
    the unions of the child type hints validating these keys and values.

    See Also
    --------
    :func:`.infer_hint_collection_items`
        Further details.
    '''
    pass


def _infer_hint_reiterable_items(
    obj: CollectionABC,
    hint_factory: object,
    conf: BeartypeConf,
    __beartype_obj_ids_seen__: FrozenSetInts,
) -> object:
    '''
    Type hint recursively validating the passed **reiterable** (i.e.,
    collections whose type hint factories are subscriptable by only a single
    child type hint) and all items transitively reachable from this reiterable,
    defined by subscripting the passed type hint factory by the union of the
    child type hints validating these items.

    See Also
    --------
    :func:`.infer_hint_collection_items`
        Further details.
    '''
    pass
