#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **Python module deprecation** utilities (i.e., callables
deprecating arbitrary module attributes in a reusable fashion).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid circular import dependencies, avoid importing from *ANY*
# package-specific submodule either here or in the body of any callable defined
# by this submodule. This submodule is typically called from the "__init__"
# submodules of public subpackages.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from typing import Any
from beartype._data.kind.datakindiota import SENTINEL
from beartype._data.kind.datakindmap import FROZENDICT_EMPTY
from collections.abc import Mapping
from warnings import warn

# ....................{ IMPORTERS                          }....................
def deprecate_module_attr(
    # Mandatory parameters.
    attr_deprecated_name: str,
    attr_nondeprecated_name_to_value: Mapping[str, Any],

    # Optional parameters.
    attr_deprecated_name_to_nondeprecated_name: Mapping[str, str] = (
        FROZENDICT_EMPTY),
) -> object:
    '''
    Dynamically retrieve a deprecated attribute with the passed unqualified name
    mapped by the passed dictionary to a corresponding non-deprecated attribute
    from the submodule with the passed dictionary of globally scoped attributes
    and emit a non-fatal deprecation warning on each such retrieval if that
    submodule defines this attribute *or* raise an exception otherwise.

    This function is intended to be called by :pep:`562`-compliant globally
    scoped ``__getattr__()`` dunder functions, which the Python interpreter
    implicitly calls under Python >= 3.7 *after* failing to directly retrieve an
    explicit attribute with this name from that submodule.

    Parameters
    ----------
    attr_deprecated_name : str
        Unqualified name of the deprecated attribute to be retrieved.
    attr_deprecated_name_to_nondeprecated_name : Mapping[str, str]
        Dictionary mapping from the unqualified name of each deprecated
        attribute retrieved by this function to either:

        * If that submodule defines a corresponding non-deprecated attribute,
          the unqualified name of that attribute.
        * If that submodule is deprecating that attribute *without* defining a
          corresponding non-deprecated attribute, :data:`None`.
    attr_nondeprecated_name_to_value : Mapping[str, object], default: FROZENDICT_EMPTY
        Dictionary mapping from the unqualified name to value of each
        module-scoped attribute defined by the caller's submodule, typically
        passed as the ``globals()`` builtin. This function intentionally does
        *not* implicitly inspect this dictionary from the call stack, as call
        stack inspection is non-portable under Python. Defaults to the empty
        frozen dictionary.

    Returns
    -------
    object
        Value of this deprecated attribute.

    Warns
    -----
    DeprecationWarning
        If this attribute is deprecated.

    Raises
    ------
    AttributeError
        If this attribute is unrecognized and thus erroneous.
    ImportError
        If the passed ``attr_nondeprecated_name_to_value`` dictionary fails to
        define the non-deprecated variant of the passed deprecated attribute
        mapped to by the passed ``attr_deprecated_name_to_nondeprecated_name``
        dictionary.

    See Also
    --------
    https://www.python.org/dev/peps/pep-0562/#id8
        :pep:`562`-compliant dunder function inspiring this implementation.
    '''
    pass
