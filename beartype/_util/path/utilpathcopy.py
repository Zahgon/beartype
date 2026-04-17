#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **path copiers** (i.e., low-level callables permanently copying
on-disk files and directories in various reasonably safe and portable ways).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeUtilPathDirException
from beartype.typing import Optional
from beartype._data.typing.datatyping import (
    CollectionStrs,
    PathnameLike,
    PathnameLikeTuple,
    TypeException,
)
from collections.abc import Callable
from pathlib import Path
from enum import (
    Enum,
    auto as next_enum_member_value,
    unique as die_unless_enum_member_values_unique,
)
from shutil import (
    copytree,
    ignore_patterns,
)

# ....................{ ENUMERATIONS                       }....................
@die_unless_enum_member_values_unique
class BeartypeDirCopyOverwritePolicy(Enum):
    '''
    Enumeration of all kinds of **directory-copying overwrite policies** (i.e.,
    competing strategies for handling edge cases in which a target path already
    exists when recursively copying directories, each with concomitant tradeoffs
    with respect to safety).

    Note that enumeration members are intentionally ordered from most safe
    (:attr:`.HALT_WITH_EXCEPTION`) to least safe (:attr:`.OVERWRITE`).

    Attributes
    ----------
    HALT_WITH_EXCEPTION : EnumMemberType
        Policy raising a fatal exception if any target path already exists. This
        constitutes the strictest and thus safest such policy.
    SKIP_WITH_WARNING : EnumMemberType
        Policy ignoring (i.e., skipping) each existing target path with a
        non-fatal warning. This policy strikes a comfortable balance between
        strictness and laxness and is thus the recommended default.
    OVERWRITE : EnumMemberType
        Policy silently overwriting each existing target path. This constitutes
        the laxest and thus riskiest such policy.
    '''

    HALT_WITH_EXCEPTION = next_enum_member_value()
    SKIP_WITH_WARNING = next_enum_member_value()
    OVERWRITE = next_enum_member_value()

# ....................{ COPIERS                            }....................
#FIXME: Unit test us up, please.
def copy_dir(
    # Mandatory parameters.
    src_dirname: PathnameLike,
    trg_dirname: PathnameLike,

    # Optional parameters.
    overwrite_policy: BeartypeDirCopyOverwritePolicy = (
        BeartypeDirCopyOverwritePolicy.HALT_WITH_EXCEPTION),
    ignore_basename_globs: Optional[CollectionStrs] = None,
    exception_cls: TypeException = _BeartypeUtilPathDirException,
    exception_prefix: str = '',
) -> None:
    '''
    Recursively copy the source directory with the passed dirname to the
    target directory with the passed dirname.

    For generality:

    * All nonexistent parents of the target directory will be recursively
      created, mimicking the action of the ``mkdir -p`` shell command on
      POSIX-compatible platforms in a platform-agnostic manner.
    * All symbolic links in the source directory will be preserved (i.e.,
      copied as is rather than their transitive targets copied instead).

    Caveats
    -------
    **This function is subject to subtle race conditions if multiple threads
    and/or processes concurrently attempt to mutate any relevant path on the
    local filesystem.** Since *all* filesystem-centric logic suffers similar
    issues, we leave this issue as an exercise for the caller.

    Parameters
    ----------
    src_dirname : PathnameLike
        Absolute or relative dirname of the source directory to be copied from.
    trg_dirname : PathnameLike
        Absolute or relative dirname of the target directory to be copied to.
    overwrite_policy : BeartypeDirCopyOverwritePolicy, default: BeartypeDirCopyOverwritePolicy.HALT_WITH_EXCEPTION
        **Directory overwrite policy** (i.e., strategy for handling existing
        paths to be overwritten by this copy). Defaults to
        :attr:`BeartypeDirCopyOverwritePolicy.HALT_WITH_EXCEPTION`, raising an
        exception if any target path already exists.
    ignore_basename_globs : Collection[str] | None, default: None
        Collection of shell-style globs (e.g., ``('*.tmp', '.keep')``) matching
        the basenames of all paths transitively owned by this source directory
        to be ignored during recursion and hence neither copied nor visited.
        Defaults to ``None``, in which case *all* paths transitively owned by
        this source directory are unconditionally copied and visited.

        Note this parameter is incompatible with the
        :attr:`BeartypeDirCopyOverwritePolicy.OVERWRITE` policy. If this
        parameter is non-:data:`None` and the ``overwrite_policy`` parameter is
        :attr:`BeartypeDirCopyOverwritePolicy.OVERWRITE`, an exception is
        raised.
    exception_cls : Type[Exception], default: _BeartypeUtilPathException
        Type of exception to be raised in the event of a fatal error. Defaults
        to :exc:`._BeartypeUtilPathException`.
    exception_prefix : str, default: ''
        Human-readable substring prefixed raised exceptions messages. Defaults
        to the empty string.

    Raises
    ------
    exception_cls
        If either:

        * The source directory does *not* exist.
        * The target directory is a subdirectory of the source directory.
          Permitting this edge case induces non-trivial issues, including
          infinite recursion from within the musty entrails of the
          :mod:`distutils` package (e.g., due to relative symbolic links).
        * The passed ``overwrite_policy`` parameter is
          :attr:`BeartypeDirCopyOverwritePolicy.HALT_WITH_EXCEPTION` *and* one or more
          subdirectories of the target directory already exist that are also
          subdirectories of the source directory. For safety, this function
          always preserves rather than overwrites existing target
          subdirectories.

    See Also
    -----------
    https://stackoverflow.com/a/22588775/2809027
        StackOverflow answer strongly inspiring this function's
        :attr:`BeartypeDirCopyOverwritePolicy.SKIP_WITH_WARNING` implementation.
    '''
    pass

# ....................{ PRIVATE ~ constants                }....................
_COPY_DIR_OVERWRITE_POLICIES_COPYTREE = frozenset((
    BeartypeDirCopyOverwritePolicy.HALT_WITH_EXCEPTION,
    BeartypeDirCopyOverwritePolicy.OVERWRITE,
))
'''
Frozen set of all **copytree-friendly directory overwrite policies** (i.e.,
:class:`.BeartypeDirCopyOverwritePolicy` enumeration members suitable for
passing as the ``overwrite_policy`` parameter to the :func:`.copy_dir` function
such that the resulting implementation reduces to a trivial call of the standard
:func:`shutil.copytree` function).
'''
