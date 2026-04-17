#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype :pep:`484`- and :pep:`585`-compliant **single-argument sequence type
hint violation finders** (i.e., functions returning human-readable strings
explaining violations of :pep:`484`- and :pep:`585`-compliant type hints
subscripted by one child type hint constraining *all* items contained in that
container satisfying the :class:`collections.abc.Container` protocol).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeCallHintPepRaiseException
from beartype._check.logic.logmap import (
    HINT_SIGN_PEP484585_CONTAINER_TO_LOGIC_get)
from beartype._check.error.errcause import ViolationCause
from beartype._check.error._nonpep.errnonpeptype import (
    find_cause_type_instance_origin)
from beartype._check.metadata.hint.hintsane import HINT_SANE_IGNORABLE
from beartype._data.hint.sign.datahintsigns import HintSignPep484585TupleFixed
from beartype._data.hint.sign.datahintsignmap import (
    HINT_SIGN_ORIGIN_ISINSTANCEABLE_TO_ARGS_LEN_RANGE)
from beartype._data.hint.sign.datahintsignset import (
    HINT_SIGNS_CONTAINER_ARGS_1)
from beartype._util.hint.pep.proposal.pep646.pep484585646tuple import (
    is_hint_pep484585646_tuple_empty)
from beartype._util.text.utiltextansi import color_type
from beartype._util.text.utiltextprefix import prefix_pith_type
from beartype._util.text.utiltextrepr import represent_pith
from collections.abc import Collection

# ....................{ FINDERS                            }....................
def find_cause_pep484585_container_args_1(
    cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the **single-argument container type hint**
    (i.e., :pep:`484`- or :pep:`585`-compliant type hint subscripted by one
    child type hint constraining *all* items contained in that container
    satisfying the :class:`collections.abc.Container` protocol) of that cause.

    Parameters
    ----------
    cause : ViolationCause
        Input violation cause finder to be inspected.

    Returns
    -------
    ViolationCause
        Output violation cause finder type-checking this input.
    '''
    pass


def find_cause_pep484585_tuple_fixed(cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the **fixed-length tuple hint** (i.e., PEP-compliant
    hint accepting zero or more subscripted arguments iteratively constraining
    each item of this fixed-length tuple) of that cause.

    Parameters
    ----------
    cause : ViolationCause
        Input violation cause finder to be inspected.

    Returns
    -------
    ViolationCause
        Output violation cause finder type-checking this input.
    '''
    pass
