#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **weak reference** (i.e., references to objects explicitly
allowing those objects to be garbage-collected at *any* time) utilities.

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeUtilPythonWeakrefException
from beartype._cave._cavefast import WeakrefCallableType
from typing import Optional

# ....................{ GETTERS                            }....................
def make_obj_weakref_and_repr(obj: object) -> tuple[Optional[WeakrefCallableType], str]:
    '''
    2-tuple ``(weakref, repr)`` weakly referring to the passed object.

    Parameters
    ----------
    obj : object
        Arbitrary object to be weakly referred to.

    Returns
    -------
    Tuple[Optional[WeakrefCallableType], str]
        2-tuple ``(weakref, repr)`` weakly referring to this object such that:

        * ``weakref`` is either:

          * If this **referent** (i.e., target object being weakly referred to)
            is the :data:`None` singleton, the :data:`._WEAKREF_NONE`
            placeholder.
          * Else if this referent supports weak references, a **weak reference**
            (i.e., :class:`weakref.ref` instance) to this object.
          * Else if this referent prohibits weak references (e.g., due to being
            a common C-based variable-sized container like a tuple or string),
            :data:`None`.

        * ``repr`` is the machine-readable representation of this object,
          truncated to ~10KB to minimize space consumption in the worst case of
          an obscenely large object.
    '''
    pass



def get_weakref_obj_or_repr(
    obj_weakref: Optional[WeakrefCallableType], obj_repr: str) -> object:
    '''
    Object weakly referred to by the passed object if this object is indeed a
    weak reference to another existing object *or* the passed machine-readable
    representation otherwise (i.e., if this object is either ``None`` *or* is a
    weak reference to a dead garbage-collected object).

    This function is typically passed the pair of objects returned by a prior
    call to the companion :func:`make_obj_weakref_and_repr` function.

    Parameters
    ----------
    obj_weakref : Optional[WeakrefCallableType]
        Either:

        * If the **referent** (i.e., target object being weakly referred to) is
          the :data:`None` singleton, the :data:`._WEAKREF_NONE` placeholder.
        * Else if the referent supports weak references, a **weak reference**
          (i.e., :class:`weakref.ref` instance) to that object.
        * Else if this referent prohibits weak references (e.g., due to being
          a common C-based variable-sized container like a tuple or string),
          :data:`None`.
    obj_repr : str
        Machine-readable representation of that object, typically truncated to
        some number of characters to avoid worst-case space consumption.

    Returns
    -------
    object
        Either:

        * If this weak reference is the :data:`_WEAKREF_NONE` placeholder, the
          ``None`` singleton.
        * Else if this referent support weak references, either:

          * If this referent is still alive (i.e., has yet to be
            garbage-collected), this referent.
          * Else, this referent is now dead (i.e., has already been
            garbage-collected). In this case, the passed representation.

        * Else, this referent does *not* support weak references (i.e., this
          weak reference is ``None``). In this case, the passed representation.

    Raises
    ----------
    _BeartypeUtilPythonWeakrefException
        If ``obj_weakref`` is invalid: i.e., neither ``None``,
        :data:`_WEAKREF_NONE`, nor a weak reference.
    '''
    pass

# ....................{ PROPERTIES ~ constants             }....................
_WEAKREF_NONE = object()
'''
Singleton substitute for the ``None`` singleton, enabling
:class:`BeartypeCallHintViolation` exceptions to differentiate between weak
references to ``None`` and weak references whose referents are already dead
(i.e., have already been garbage-collected).
'''
