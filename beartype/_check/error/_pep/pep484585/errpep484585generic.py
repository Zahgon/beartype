#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype PEP-compliant generic type hint exception raisers** (i.e., functions
raising human-readable exceptions called by :mod:`beartype`-decorated callables
on the first invalid parameter or return value failing a type-check against the
PEP-compliant generic type hint annotating that parameter or return).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype._data.hint.sign.datahintsigns import (
    HintSignPep484585GenericUnsubbed)
from beartype._check.error.errcause import ViolationCause
from beartype._check.error._nonpep.errnonpeptype import (
    find_cause_instance_type)
from beartype._check.pep.checkpep484585generic import (
    get_hint_pep484585_generic_unsubbed_bases_unerased_kwargs)
from beartype._util.hint.pep.proposal.pep484585.generic.pep484585genget import (
    get_hint_pep484585_generic_type_isinstanceable)
from beartype._util.text.utiltextansi import color_hint

# ....................{ GETTERS                            }....................
def find_cause_pep484585_generic_unsubbed(
    cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the :pep:`484`- or :pep:`585`-compliant
    **unsubscripted generic** (i.e., type hint subclassing a combination of one
    or more of the :mod:`typing.Generic` superclass, the :mod:`typing.Protocol`
    superclass, and/or other :mod:`typing` non-class pseudo-superclasses) of
    that cause.

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
