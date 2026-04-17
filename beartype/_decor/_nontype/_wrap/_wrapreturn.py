#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype decorator return code generator** (i.e., low-level callables
dynamically generating Python expressions type-checking the annotated return of
the callable currently being decorated by the :func:`beartype.beartype`
decorator in a general-purpose manner).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype._check.checkmake import (
    make_code_raiser_func_pith_check,
    make_code_raiser_func_pep484_noreturn_check,
)
from beartype._check.convert.convmain import sanify_hint_root_func
from beartype._check.metadata.call.callmetadecor import (
    BeartypeCallDecorMeta,
    prefix_decor_meta_callable_return,
)
from beartype._check.metadata.hint.hintsane import HINT_SANE_IGNORABLE
from beartype._data.code.func.datacodefuncwrap import CODE_CALL_CHECKED_format
from beartype._data.code.pep.datacodepep484 import PEP484_CODE_CHECK_NORETURN
from beartype._data.error.dataerrmagic import EXCEPTION_PLACEHOLDER
from beartype._data.func.datafuncarg import ARG_NAME_RETURN
from beartype._data.kind.datakindiota import SENTINEL
from beartype._data.typing.datatyping import LexicalScope
from beartype._data.typing.datatypingport import Hint
from beartype._util.error.utilerrraise import reraise_exception_placeholder
from beartype._util.error.utilerrwarn import reissue_warnings_placeholder
from beartype._util.kind.maplike.utilmapset import update_mapping
from typing import NoReturn
from warnings import catch_warnings

# ....................{ CODERS                             }....................
def code_check_return(decor_meta: BeartypeCallDecorMeta) -> str:
    '''
    Generate a Python code snippet type-checking the annotated return declared
    by the decorated callable if any *or* the empty string otherwise (i.e., if
    this return is unannotated).

    Parameters
    ----------
    decor_meta : BeartypeCallDecorMeta
        Decorated callable to be type-checked.

    Returns
    -------
    str
        Code type-checking any annotated return of the decorated callable.

    Raises
    ------
    BeartypeDecorHintPep484585Exception
        If this callable is either:

        * A coroutine *not* annotated by a :obj:`typing.Coroutine` type hint.
        * A generator *not* annotated by a :obj:`typing.Generator` type hint.
        * An asynchronous generator *not* annotated by a
          :obj:`typing.AsyncGenerator` type hint.
    BeartypeDecorHintNonpepException
        If the type hint annotating this return (if any) of this callable is
        neither:

        * **PEP-compliant** (i.e., :mod:`beartype`-agnostic hint compliant with
          annotation-centric PEPs).
        * **PEP-noncompliant** (i.e., :mod:`beartype`-specific type hint *not*
          compliant with annotation-centric PEPs)).
    '''
    pass
