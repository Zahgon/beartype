#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype :pep:`484`- and :pep:`585`-compliant **mapping type hint violation
describers** (i.e., functions returning human-readable strings explaining
violations of :pep:`484`- and :pep:`585`-compliant mapping type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype import BeartypeStrategy
from beartype.typing import (
    Hashable,
    Iterable,
    Tuple,
)
from beartype._check.error.errcause import ViolationCause
from beartype._check.error._nonpep.errnonpeptype import (
    find_cause_type_instance_origin)
from beartype._check.metadata.hint.hintsane import HINT_SANE_IGNORABLE
from beartype._data.hint.sign.datahintsignmap import (
    HINT_SIGN_ORIGIN_ISINSTANCEABLE_TO_ARGS_LEN_RANGE)
from beartype._data.hint.sign.datahintsigns import HintSignCounter
from beartype._data.hint.sign.datahintsignset import HINT_SIGNS_MAPPING
from beartype._util.text.utiltextprefix import prefix_pith_type
from beartype._util.text.utiltextrepr import represent_pith

# ....................{ FINDERS                            }....................
def find_cause_pep484585_mapping(cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either
    satisfies or violates the **mapping type hint** (i.e., PEP-compliant type
    hint accepting exactly two subscripted arguments constraining *all*
    key-value pairs of this pith, which necessarily satisfies the
    :class:`collections.abc.Mapping` protocol) of that cause.

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
