#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **Decidedly Object-Oriented Runtime-checking (DOOR) subscripted type
hint classes** (i.e., :class:`beartype.door.TypeHint` subclasses implementing
support for :pep:`484`- and :pep:`585`-compliant subscripted type hints *not*
already matched by any more fine-grained :class:`beartype.door.TypeHint`
subclass).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.door._cls.doorsuper import TypeHint
from beartype.roar import BeartypeDoorPepArgsLenException
from beartype._data.hint.sign.datahintsignmap import (
    HINT_SIGN_ORIGIN_ISINSTANCEABLE_TO_ARGS_LEN_RANGE)

# ....................{ SUBCLASSES                         }....................
class SubscriptedTypeHint(TypeHint):
    '''
    **Subscripted type hint wrapper** (i.e., high-level object encapsulating
    a low-level parent type hint satisfying various conditions).

    Notably, this wrapper wraps hints that both:

    * Are either :pep:`484`- or :pep:`585`-compliant.
    * Are subscripted (indexed) by a predetermined number of one or more
      low-level child type hints.
    * Originate from an **isinstanceable class** such that *all* objects
      satisfying this hint are instances of that class.
    '''

    # ..................{ PRIVATE ~ factories                }..................
    def _make_args(self) -> tuple:

        # Tuple of the zero or more low-level child type hints subscripting
        # (indexing) the low-level parent type hint wrapped by this wrapper.
        pass

    # ..................{ PRIVATE ~ testers                  }..................
    # Note that this redefinition of the superclass _is_equal() method is
    # technically unnecessary, as that method is already sufficiently
    # general-purpose to suffice for *ALL* possible subclasses (including this
    # subclass). Nonetheless, we wrote this method first. More importantly, this
    # method is *SUBSTANTIALLY* faster than the superclass method. Although
    # efficiency is typically *NOT* a pressing concern for the DOOR API,
    # discarding faster working code would be senseless.
    def _is_equal(self, other: TypeHint) -> bool:

        # If *ALL* of the child type hints subscripting both of these parent
        # type hints are ignorable, return true only if these parent type hints
        # both originate from the same isinstanceable class.
        pass
