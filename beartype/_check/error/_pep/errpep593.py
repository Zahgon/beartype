#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype :pep:`593`-compliant **type hint violation describers** (i.e.,
functions returning human-readable strings explaining violations of
:pep:`593`-compliant :obj:`typing.Annotated` type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeCallHintPepRaiseException
from beartype._check.error.errcause import ViolationCause
from beartype._data.hint.sign.datahintsigns import HintSignAnnotated
from beartype._util.hint.pep.proposal.pep593 import (
    get_hint_pep593_metadata,
    get_hint_pep593_metahint,
)
from beartype._data.code.datacodeindent import CODE_INDENT_1
from beartype._util.text.utiltextrepr import represent_pith

# ....................{ FINDERS                            }....................
def find_cause_pep593_annotated(cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the :pep:`593`-compliant :mod:`beartype`-specific
    **metahint** (i.e., type hint annotating a standard class with one or more
    :class:`beartype.vale._core._valecore.BeartypeValidator` objects, each
    produced by subscripting the :class:`beartype.vale.Is` class or a subclass
    of that class) of that cause.

    Parameters
    ----------
    cause : ViolationCause
        Input cause providing this data.

    Returns
    -------
    ViolationCause
        Output cause type-checking this data.
    '''
    pass
