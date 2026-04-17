#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype** :pep:`586`-compliant **type hint violation describers** (i.e.,
functions returning human-readable strings explaining violations of
:pep:`586`-compliant :attr:`typing.Literal` type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype._check.error.errcause import ViolationCause
from beartype._data.hint.sign.datahintsigns import HintSignLiteral
from beartype._util.hint.pep.proposal.pep586 import get_hint_pep586_literals
from beartype._util.text.utiltextansi import color_type
from beartype._util.text.utiltextjoin import join_delimited_disjunction
from beartype._util.text.utiltextrepr import represent_pith

# ....................{ GETTERS                            }....................
def find_cause_pep586_literal(cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the :pep:`586`-compliant :mod:`beartype`-specific
    **literal** (i.e., :obj:`typing.Literal` type hint) of that cause.

    Parameters
    ----------
    cause : ViolationCause
        Input cause providing this data.

    Returns
    ----------
    ViolationCause
        Output cause type-checking this data.
    '''
    pass
