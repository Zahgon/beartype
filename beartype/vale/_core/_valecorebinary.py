#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
**Core unary beartype validators** (i.e., :class:`BeartypeValidator` subclasses
implementing binary operations on pairs of lower-level beartype validators).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from abc import ABCMeta, abstractmethod
from beartype.roar import BeartypeValeSubscriptionException
from beartype.vale._core._valecore import BeartypeValidator
from beartype.vale._util._valeutiltext import format_diagnosis_line
from beartype._util.kind.maplike.utilmapset import merge_mappings_two
from beartype._data.code.datacodeindent import CODE_INDENT_1
from beartype._util.text.utiltextrepr import represent_object

# ....................{ SUPERCLASSES                       }....................
class BeartypeValidatorBinaryABC(BeartypeValidator, metaclass=ABCMeta):
    '''
    Abstract base class of all **beartype binary validator** (i.e., validator
    modifying the boolean truthiness returned by the validation performed by a
    pair of lower-level beartype validators) subclasses.

    Attributes
    ----------
    _validator_operand_1 : BeartypeValidator
        First lower-level validator operated upon by this higher-level
        validator.
    _validator_operand_2 : BeartypeValidator
        Second lower-level validator operated upon by this higher-level
        validator.
    '''

    # ..................{ CLASS VARIABLES                    }..................
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CAUTION: Subclasses declaring uniquely subclass-specific instance
    # variables *MUST* additionally slot those variables. Subclasses violating
    # this constraint will be usable but unslotted, which defeats our purposes.
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Slot all instance variables defined on this object to minimize the time
    # complexity of both reading and writing variables across frequently called
    # cache dunder methods. Slotting has been shown to reduce read and write
    # costs by approximately ~10%, which is non-trivial.
    __slots__ = (
        '_validator_operand_1',
        '_validator_operand_2',
    )

    # ..................{ INITIALIZERS                       }..................
    def __init__(
        self,
        validator_operand_1: BeartypeValidator,
        validator_operand_2: BeartypeValidator,
        **kwargs
    ) -> None:
        '''
        Initialize this higher-level validator from the passed validators.

        Parameters
        ----------
        validator_operand_1 : BeartypeValidator
            First validator operated upon by this higher-level validator.
        validator_operand_2 : BeartypeValidator
            Second validator operated upon by this higher-level validator.

        All remaining parameters are passed as is to the superclass
        :meth:`BeartypeValidator.__init__` method.

        Raises
        ----------
        BeartypeValeSubscriptionException
            If either of these operands are *not* beartype validators.
        '''

        # Locals safely merging the locals required by the code provided by
        # both validators.
        is_valid_code_locals = merge_mappings_two(
            validator_operand_1._is_valid_code_locals,
            validator_operand_2._is_valid_code_locals,
        )

        # Callable accepting no arguments returning a machine-readable
        # representation of this binary validator.
        get_repr = lambda: (
            f'{repr(validator_operand_1)} {self._operator_symbol} '
            f'{repr(validator_operand_2)}'
        )

        # Initialize our superclass with all remaining parameters.
        super().__init__(
            is_valid_code_locals=is_valid_code_locals,  # type: ignore[arg-type]
            get_repr=get_repr,
            **kwargs
        )

        # Classify all remaining parameters.
        self._validator_operand_1 = validator_operand_1
        self._validator_operand_2 = validator_operand_2

    # ..................{ GETTERS                            }..................
    #FIXME: Unit test us up, please.
    #FIXME: Overly verbose for conjunctions involving three or more
    #beartype validators. Contemplate compaction schemes, please. Specifically,
    #we need to detect this condition here and then compact based on that:
    #    # If either of these validators are themselves conjunctions...
    #    if isinstance(self._validator_operand_1, BeartypeValidatorConjunction):
    #       ...
    #    if isinstance(self._validator_operand_2, BeartypeValidatorConjunction):
    #       ...
    def get_diagnosis(
        self,
        *,

        # Mandatory keyword-only parameters.
        obj: object,
        indent_level_outer: str,
        indent_level_inner: str,

        # Optional keyword-only parameters.
        is_shortcircuited: bool = False,
    ) -> str:

        # Innermost indentation level indented one level deeper than the passed
        # innermost indentation level.
        pass

    # ..................{ ABSTRACT                           }..................
    # Abstract methods required to be concretely implemented by subclasses.

    @property
    @abstractmethod
    def _operator_symbol(self) -> str:
        '''
        Human-readable string embodying the operation performed by this binary
        validator - typically the single-character mathematical sign
        symbolizing this operation.
        '''

        pass


    @abstractmethod
    def _is_shortcircuited(self, obj: object) -> bool:
        '''
        ``True`` only if the first child validator short-circuits the second
        child validator underlying this parent validator with respect to the
        passed object.

        In this context, "short-circuits" is in the boolean evaluation sense.
        Specifically, short-circuiting:

        * Occurs when the first child validator either fully satisfies or
          violates this parent validator with respect to the passed object.
        * Implies the second child validator to be safely ignorable with
          respect to the passed object.

        Parameters
        ----------
        obj : object
            Arbitrary object to be diagnosed against this validator.

        Returns
        ----------
        bool
            ``True`` only if this the passed object short-circuits the second
            child operand validator underlying this parent binary validator.
        '''

        pass

# ....................{ SUBCLASSES ~ &                     }....................
class BeartypeValidatorConjunction(BeartypeValidatorBinaryABC):
    '''
    **Beartype conjunction validator** (i.e., validator conjunctively
    evaluating the boolean truthiness returned by the validation performed by a
    pair of lower-level beartype validators, typically instantiated and
    returned by the :meth:`BeartypeValidator.__and__` dunder method of the
    first validator passed the second).
    '''

    # ..................{ INITIALIZERS                       }..................
    def __init__(
        self,
        validator_operand_1: BeartypeValidator,
        validator_operand_2: BeartypeValidator,
    ) -> None:
        '''
        Initialize this higher-level validator from the passed validators.

        Parameters
        ----------
        validator_operand_1 : BeartypeValidator
            First validator operated upon by this higher-level validator.
        validator_operand_2 : BeartypeValidator
            Second validator operated upon by this higher-level validator.

        Raises
        ----------
        BeartypeValeSubscriptionException
            If either of these operands are *not* beartype validators.
        '''

        # Validate the passed operands as sane.
        _validate_operands(self, validator_operand_1, validator_operand_2)

        # Initialize our superclass with all remaining parameters.
        super().__init__(
            validator_operand_1=validator_operand_1,
            validator_operand_2=validator_operand_2,
            # Lambda function conjunctively performing both validations.
            is_valid=lambda obj: (
                validator_operand_1.is_valid(obj) and
                validator_operand_2.is_valid(obj)
            ),
            # Code expression conjunctively performing both validations.
            is_valid_code=(
                f'({validator_operand_1._is_valid_code} and '
                f'{validator_operand_2._is_valid_code})'
            ),
        )

    # ..................{ PROPERTIES                         }..................
    @property
    def _operator_symbol(self) -> str:
        pass


    def _is_shortcircuited(self, obj: object) -> bool:

        # Return true only if the passed object violates this first child
        # validator. Why? Because if this first child validator is violated,
        # then this parent validator as a whole is violated; no further
        # validation of this second child validator is required.
        pass

# ....................{ SUBCLASSES ~ |                     }....................
class BeartypeValidatorDisjunction(BeartypeValidatorBinaryABC):
    '''
    **Beartype disjunction validator** (i.e., validator disjunctively
    evaluating the boolean truthiness returned by the validation performed by a
    pair of lower-level beartype validators, typically instantiated and
    returned by the :meth:`BeartypeValidator.__and__` dunder method of the
    first validator passed the second).
    '''

    # ..................{ INITIALIZERS                       }..................
    def __init__(
        self,
        validator_operand_1: BeartypeValidator,
        validator_operand_2: BeartypeValidator,
    ) -> None:
        '''
        Initialize this higher-level validator from the passed validators.

        Parameters
        ----------
        validator_operand_1 : BeartypeValidator
            First validator operated upon by this higher-level validator.
        validator_operand_2 : BeartypeValidator
            Second validator operated upon by this higher-level validator.

        Raises
        ----------
        BeartypeValeSubscriptionException
            If either of these operands are *not* beartype validators.
        '''

        # Validate the passed operands as sane.
        _validate_operands(self, validator_operand_1, validator_operand_2)

        # Initialize our superclass with all remaining parameters.
        super().__init__(
            validator_operand_1=validator_operand_1,
            validator_operand_2=validator_operand_2,
            # Lambda function disjunctively performing both validations.
            is_valid=lambda obj: (
                validator_operand_1.is_valid(obj) or
                validator_operand_2.is_valid(obj)
            ),
            # Code expression disjunctively performing both validations.
            is_valid_code=(
                f'({validator_operand_1._is_valid_code} or '
                f'{validator_operand_2._is_valid_code})'
            ),
        )

    # ..................{ PROPERTIES                         }..................
    @property
    def _operator_symbol(self) -> str:
        pass


    def _is_shortcircuited(self, obj: object) -> bool:

        # Return true only if the passed object satisfies this first child
        # validator. Why? Because if this first child validator is satisfied,
        # then this parent validator as a whole is satisfied; no further
        # validation of this second child validator is required.
        pass

# ....................{ PRIVATE ~ validators               }....................
def _validate_operands(
    self: BeartypeValidatorBinaryABC,
    validator_operand_1: BeartypeValidator,
    validator_operand_2: BeartypeValidator,
) -> None:
    '''
    Validate the passed validator operands as sane.

    Parameters
    ----------
    self : BeartypeValidatorBinaryABC
        Beartype binary validator operating upon these operands.
    validator_operand_1 : BeartypeValidator
        First validator operated upon by this higher-level validator.
    validator_operand_2 : BeartypeValidator
        Second validator operated upon by this higher-level validator.

    Raises
    ----------
    BeartypeValeSubscriptionException
        If either of these operands are *not* beartype validators.
    '''
    pass
    # Else, both of these operands are beartype validators.
