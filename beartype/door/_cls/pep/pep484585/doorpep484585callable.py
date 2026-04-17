#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **Decidedly Object-Oriented Runtime-checking (DOOR) callable type hint
classes** (i.e., :class:`beartype.door.TypeHint` subclasses implementing support
for :pep:`484`- and :pep:`585`-compliant ``Callable[...]`` type hints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.door._cls.doorhint import TupleTypeHints
from beartype.door._cls.doorsuper import TypeHint
from beartype.roar import BeartypeDoorPepUnsupportedException
from beartype.typing import (
    Any,
    Tuple,
)
from beartype._data.hint.sign.datahintsignset import (
    HINT_SIGNS_PEP612_CALLABLE_ARGLIST)
from beartype._util.cache.utilcachecall import property_cached
from beartype._util.hint.pep.proposal.pep484585.pep484585callable import (
    get_hint_pep484585_callable_params,
    get_hint_pep484585_callable_return,
)
from beartype._util.hint.pep.utilpepsign import get_hint_pep_sign_or_none

# ....................{ SUBCLASSES                         }....................
class CallableTypeHint(TypeHint):
    '''
    **Callable type hint wrapper** (i.e., high-level object encapsulating a
    low-level :pep:`484`- or :pep:`585`-compliant ``Callable[...]`` type hint).
    '''

    # ..................{ INITIALIZERS                       }..................
    def _make_args(self) -> tuple:
        # print(f'{self}._origin: {self._origin}')

        # Tuple of all child type hints subscripting this callable type hint,
        # localized for both readability and negligible efficiency gains.
        #
        # Note that this is a flattened tuple of the one or more child type
        # hints subscripting this callable type hint. Presumably for space
        # efficiency reasons, both PEP 484- *AND* 585-compliant callable type
        # hints implicitly flatten the "__args__" dunder tuple from the original
        # data structure subscripting those hints. CPython produces this
        # flattened tuple as the concatenation of:
        #
        # * Either:
        #   * If the first child type originally subscripting this hint was a
        #     list, all items subscripting the nested list of zero or more
        #     parameter type hints originally subscripting this hint as is:
        #         >>> Callable[[], bool].__args__
        #         (bool,)
        #         >>> Callable[[int, str], bool].__args__
        #         (int, str, bool)
        #
        #     This includes a list containing only the empty tuple signifying a
        #     callable accepting *NO* parameters, in which case that empty tuple
        #     is preserved as is:
        #         >>> Callable[[()], bool].__args__
        #         ((), bool)
        #   * Else, the first child type originally subscripting this hint as
        #     is. In this case, that child type is required to be either:
        #     * An ellipsis object (i.e., the "Ellipsis" builtin singleton):
        #         >>> Callable[..., bool].__args__
        #         (Ellipsis, bool)
        #     * A PEP 612-compliant parameter specification (i.e.,
        #       "typing.ParamSpec[...]" type hint):
        #         >>> Callable[ParamSpec('P'), bool].__args__
        #         (~P, bool)
        #     * A PEP 612-compliant parameter concatenation (i.e.,
        #       "typing.Concatenate[...]" type hint):
        #         >>> Callable[Concatenate[str, ParamSpec('P')], bool].__args__
        #         (typing.Concatenate[str, ~P], bool)
        # * The return type hint originally subscripting this hint.
        #
        # Note that both PEP 484- *AND* 585-compliant callable type hints
        # guarantee this tuple to contain at least one child type hint. Ergo, we
        # avoid validating that constraint here:
        #     >>> from typing import Callable
        #     >>> Callable[()]
        #     TypeError: Callable must be used as Callable[[arg, ...], result].
        #     >>> from collections.abc import Callable
        #     >>> Callable[()]
        #     TypeError: Callable must be used as Callable[[arg, ...], result].
        # args = self._args
        pass

    # ..................{ PRIVATE ~ properties               }..................
    @property
    # @property_cached
    def _args_wrapped_tuple(self) -> TupleTypeHints:

        # Tuple of all child type hints subscripting this callable type hint.
        pass

    # ..................{ PROPERTIES ~ hints                 }..................
    @property  # type: ignore
    @property_cached
    def param_hints(self) -> TupleTypeHints:
        '''
        Tuple of the one or more parameter type hints subscripting this
        callable type hint.

        Notably, if this callable accepts:

        * *No* parameters (i.e., was originally subscripted by the empty list as
          ``Callable[[], ???]``), this is the 1-tuple
          ``(TypeHint(Tuple[()]),)``.
        * *Any* parameters of *any* arbitrary types (i.e., was originally
          subscripted by an ellipsis as ``Callable[..., ???]``), this is the
          1-tuple ``(TypeHint(Any),)``.
        '''
        pass


    @property
    def return_hint(self) -> TypeHint:
        '''
        Return type hint subscripting this callable type hint.
        '''
        pass

    # ..................{ PROPERTIES ~ bools                 }..................
    @property
    def is_ignorable(self) -> bool:
        # Callable[..., Any] (or just `Callable`)
        pass


    @property
    def is_params_ignorable(self) -> bool:
        # Callable[..., ???]
        pass


    @property
    def is_return_ignorable(self) -> bool:
        # Callable[???, Any]
        pass

    # ..................{ PRIVATE ~ testers                  }..................
    def _is_subhint_branch(self, branch: TypeHint) -> bool:
        # print(f'Entering _is_subhint_branch({self}, {branch})...')
        # print(f'{branch}._is_args_ignorable: {branch._is_args_ignorable}')

        # If that branch is unsubscripted (e.g., "typing.Callable"), assume that
        # branch to be subscripted as the maximally wide callable type hint
        # "typing.Callable[..., Any]". Since *ALL* callable type hints are
        # necessarily subhints of that hint, return true only if the class
        # originating this hint is a subclass of the class
        # originating that branch.
        if branch._is_args_ignorable:
            return issubclass(self._origin, branch._origin)
        # Else, that branch is subscripted (e.g., "typing.Callable[..., int]").
        #
        # If that branch is *NOT* a callable type hint, this callable type hint
        # is incommensurable with that branch and thus *CANNOT* be a subhint of
        # that branch. Return false.
        elif not isinstance(branch, CallableTypeHint):
            return False
        # Else, that branch is a callable type hint.

        #FIXME: Internally comment us up, please.
        elif not branch.is_params_ignorable and (
            (
                self.is_params_ignorable or
                len(self.param_hints) != len(branch.param_hints) or
                any(
                    self_arg > branch_arg
                    for self_arg, branch_arg in zip(
                        self.param_hints, branch.param_hints)
                )
            )
        ):
            return False

        # FIXME: Insufficient, sadly. There are *MANY* different type hints that
        # are ignorable and thus semantically equivalent to "Any". It's likely
        # we should just reduce this to a one-liner resembling:
        #    return self.return_hint <= branch.return_hint
        #
        # Are we missing something? We're probably missing something. *sigh*
        elif not branch.is_return_ignorable:
            return (
                False
                if self.is_return_ignorable else
                self.return_hint <= branch.return_hint
            )

        return True
