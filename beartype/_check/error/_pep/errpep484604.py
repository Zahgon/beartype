#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype** :pep:`484`-compliant **union type hint violation describers**
(i.e., functions returning human-readable strings explaining violations of
:pep:`484`-compliant union type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeCallHintPepRaiseException
from beartype._data.hint.sign.datahintsignset import HINT_SIGNS_UNION
from beartype._check.error.errcause import ViolationCause
from beartype._check.metadata.hint.hintsane import HINT_SANE_IGNORABLE
from beartype._util.hint.pep.utilpepget import (
    get_hint_pep_origin_type_isinstanceable_or_none)
from beartype._util.hint.pep.utilpeptest import is_hint_pep
from beartype._util.text.utiltextjoin import join_delimited_disjunction_types
from beartype._util.text.utiltextmunge import (
    suffix_str_unless_suffixed,
    uppercase_str_char_first,
)
from beartype._util.text.utiltextrepr import represent_pith

# ....................{ GETTERS                            }....................
def find_cause_pep484604_union(cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the PEP-compliant union type hint of that cause.

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
