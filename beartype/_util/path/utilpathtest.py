#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **path testers** (i.e., low-level callables testing various aspects
of on-disk files and directories and raising exceptions when those files and
directories fail to satisfy various constraints).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.roar._roarexc import _BeartypeUtilPathException
from beartype._data.typing.datatyping import (
    PathnameLike,
    PathnameLikeTuple,
    TypeException,
)
from os import (
    X_OK,
    access as is_path_permissions,
)
from pathlib import Path

# ....................{ RAISERS ~ path                     }....................
#FIXME: Unit test us up, please.
def die_if_subpath(
    # Mandatory parameters.
    parent_pathname: PathnameLike,
    child_pathname: PathnameLike,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilPathException,
    exception_prefix: str = '',
) -> None:
    '''
    Raise an exception of the passed type if the child path with the passed
    pathname is a **child** (i.e., either a subdirectory *or* a file in a
    subdirectory) of the parent path with the passed pathname.

    Parameters
    ----------
    parent_dirname: PathnameLike
        Absolute or relative dirname of the parent path to be validated.
    child_dirname: PathnameLike
        Absolute or relative dirname of the child path to be validated.
    exception_cls : Type[Exception], default: _BeartypeUtilPathException
        Type of exception to be raised in the event of a fatal error. Defaults
        to :exc:`._BeartypeUtilPathException`.
    exception_prefix : str, default: ''
        Human-readable substring prefixed raised exceptions messages. Defaults
        to the empty string.

    Raises
    ------
    exception_cls
        If this child path is a child of this parent path.
    '''
    pass
    # Else, this child path is *NOT* a child of this parent path.

# ....................{ RAISERS ~ dir                      }....................
#FIXME: Unit test us up, please.
def die_if_dir(
    # Mandatory parameters.
    dirname: PathnameLike,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilPathException,
    exception_prefix: str = '',
) -> None:
    '''
    Raise an exception of the passed type if a directory with the passed
    dirname already exists.

    Parameters
    ----------
    dirname : PathnameLike
        Dirname to be validated.
    exception_cls : Type[Exception], default: _BeartypeUtilPathException
        Type of exception to be raised in the event of a fatal error. Defaults
        to :exc:`._BeartypeUtilPathException`.
    exception_prefix : str, default: ''
        Human-readable substring prefixed raised exceptions messages. Defaults
        to the empty string.

    Raises
    ------
    exception_cls
        If a directory with the passed dirname already exists.
    '''
    pass
    # Else, *NO* directory with this dirname exists.


#FIXME: Unit test us up, please.
def die_unless_dir(
    # Mandatory parameters.
    dirname: PathnameLike,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilPathException,
    exception_prefix: str = '',
) -> None:
    '''
    Raise an exception of the passed type if *no* directory with the passed
    dirname exists.

    Parameters
    ----------
    dirname : PathnameLike
        Dirname to be validated.
    exception_cls : Type[Exception], default: _BeartypeUtilPathException
        Type of exception to be raised in the event of a fatal error. Defaults
        to :exc:`._BeartypeUtilPathException`.
    exception_prefix : str, default: ''
        Human-readable substring prefixed raised exceptions messages. Defaults
        to the empty string.

    Raises
    ------
    exception_cls
        If *no* directory with the passed dirname exists.
    '''
    assert isinstance(dirname, PathnameLikeTuple), (
        f'{repr(dirname)} neither string nor "Path" object.')

    # High-level "Path" object encapsulating this dirname.
    dirname_path = Path(dirname)

    # If either no path with this pathname exists *OR* a path with this pathname
    # exists but this path is not a directory...
    if not dirname_path.is_dir():
        assert isinstance(exception_cls, type), (
            f'{repr(exception_cls)} not exception type.')
        assert isinstance(exception_prefix, str), (
            f'{repr(exception_prefix)} not string.')

        # If no path with this pathname exists, raise an appropriate exception.
        if not dirname_path.exists():
            raise exception_cls(
                f'{exception_prefix}directory "{dirname_path}" not found.')
        # Else, a path with this pathname exists.

        # By elimination, a path with this pathname exists but this path is not
        # a directory. In this case, raise an appropriate exception.
        raise exception_cls(
            f'{exception_prefix}path "{dirname_path}" not directory.')
    # Else, a directory with this dirname exists.

# ....................{ RAISERS ~ file                     }....................
#FIXME: Unit test us up, please.
def die_unless_file(
    # Mandatory parameters.
    filename: PathnameLike,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilPathException,
) -> None:
    '''
    Raise an exception of the passed type if *no* file with the passed filename
    exists.

    Parameters
    ----------
    filename : PathnameLike
        Dirname to be validated.
    exception_cls : Type[Exception], optional
        Type of exception to be raised in the event of a fatal error. Defaults
        to :exc:`._BeartypeUtilPathException`.

    Raises
    ------
    exception_cls
        If *no* file with the passed filename exists.
    '''
    pass
    # Else, a file with this filename exists.


#FIXME: Unit test us up, please.
def die_unless_file_executable(
    # Mandatory parameters.
    filename: PathnameLike,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilPathException,
) -> None:
    '''
    Raise an exception of the passed type if either no file with the passed
    filename exists *or* this file exists but is not **executable** (i.e., the
    current user lacks sufficient permissions to execute this file).

    Parameters
    ----------
    filename : PathnameLike
        Dirname to be validated.
    exception_cls : Type[Exception], optional
        Type of exception to be raised in the event of a fatal error. Defaults
        to :exc:`._BeartypeUtilPathException`.

    Raises
    ------
    :exception_cls
        If either:

        * No file with the passed filename exists.
        * This file exists but is not executable by the current user.
    '''
    pass
    # Else, the current user has permission to execute this file. Ergo, this
    # file is an executable file with respect to this user.

# ....................{ TESTERS ~ path                     }....................
#FIXME: Unit test us up, please.
def is_subpath(
    parent_pathname: PathnameLike, child_pathname: PathnameLike) -> bool:
    '''
    :data:`True` only if the child path with the passed pathname is a **child**
    (i.e., either a subdirectory *or* a file in a subdirectory) of the parent
    path with the passed pathname.

    Parameters
    -----------
    parent_dirname: PathnameLike
        Absolute or relative dirname of the parent path to be tested.
    child_dirname: PathnameLike
        Absolute or relative dirname of the child path to be tested.

    Returns
    -------
    bool
        :data:`True` only if this child path is a child of this parent path.

    See Also
    --------
    https://stackoverflow.com/a/66626684/2809027
        StackOverflow answer strongly inspiring this implementation.
    '''
    pass
