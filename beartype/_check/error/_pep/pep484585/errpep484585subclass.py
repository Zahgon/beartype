#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype :pep:`484`-compliant :attr:`typing.NoReturn` **type hint violation
describers** (i.e., functions returning human-readable strings explaining
violations of :pep:`484`-compliant :attr:`typing.NoReturn` type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeCallHintPepRaiseException
from beartype._check.error.errcause import ViolationCause
from beartype._check.metadata.hint.hintsane import HINT_SANE_IGNORABLE
from beartype._data.typing.datatyping import TypeOrTupleTypes
from beartype._data.hint.sign.datahintsigns import (
    HintSignType,
    HintSignUnion,
)
from beartype._util.cls.pep.clspep3119 import die_unless_object_issubclassable
from beartype._util.cls.utilclstest import is_type_subclass
from beartype._util.hint.pep.utilpepget import get_hint_pep_args
from beartype._util.hint.pep.utilpepsign import get_hint_pep_sign_or_none
from beartype._util.text.utiltextjoin import join_delimited_disjunction_types
from beartype._util.text.utiltextlabel import label_type
from beartype._util.text.utiltextrepr import represent_pith

# ....................{ GETTERS                            }....................
def find_cause_pep484585_subclass(cause: ViolationCause) -> ViolationCause:
    '''
    Output cause describing whether the pith of the passed input cause either is
    or is not a subclass of the issubclassable type of that cause.

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
