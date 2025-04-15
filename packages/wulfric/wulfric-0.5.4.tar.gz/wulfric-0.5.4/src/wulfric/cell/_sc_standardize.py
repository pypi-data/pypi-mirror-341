# Wulfric - Cell, Atoms, K-path.
# Copyright (C) 2023-2025 Andrey Rybakov
#
# e-mail: anry@uv.es, web: adrybakov.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np

from wulfric._exceptions import StandardizationTypeMismatch
from wulfric._numerical import compare_numerically
from wulfric.cell._basic_manipulation import (
    get_params,
    get_reciprocal,
    get_scalar_products,
)
from wulfric.cell._lepage import lepage
from wulfric.constants._sc_notation import C_MATRICES

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _CUB_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary cubic cell returns matrix S that transforms it to the standardized form.

    See :ref:`guide_cub` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`.

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the cubic lattice.
    If the cell is not cubic, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _FCC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary face-centered cubic cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_fcc` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`.

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the face-centered cubic lattice.
    If the cell is not face-centered cubic, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _BCC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary body-centered cubic cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_fcc` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`.

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the body-centered cubic lattice.
    If the cell is not body-centered cubic, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _TET_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary tetragonal cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_tet` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the tetragonal lattice. If the
    cell is not tetragonal, the function will not work correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the tetragonal conditions are satisfied.
    """

    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(a, "==", b, eps=length_tolerance) and compare_numerically(
        b, "!=", c, eps=length_tolerance
    ):
        S = np.eye(3, dtype=float)
    elif compare_numerically(b, "==", c, eps=length_tolerance) and compare_numerically(
        c, "!=", a, eps=length_tolerance
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(a, "==", c, eps=length_tolerance) and compare_numerically(
        c, "!=", b, eps=length_tolerance
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("tetragonal")

    return S


def _BCT_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary body-centered tetragonal cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_bct` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the body-centered tetragonal
    lattice. If the cell is not body-centered tetragonal, the function will not work
    correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the body-centered tetragonal conditions are satisfied.
    """
    cell = np.array(cell)

    _, _, _, alpha, beta, gamma = get_params(cell)

    if compare_numerically(
        alpha, "==", beta, eps=angle_tolerance
    ) and compare_numerically(beta, "!=", gamma, eps=angle_tolerance):
        S = np.eye(3, dtype=float)
    elif compare_numerically(
        beta, "==", gamma, eps=angle_tolerance
    ) and compare_numerically(gamma, "!=", alpha, eps=angle_tolerance):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(
        alpha, "==", gamma, eps=angle_tolerance
    ) and compare_numerically(gamma, "!=", beta, eps=angle_tolerance):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("body-centered tetragonal")

    return S


def _ORC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary orthorhombic cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_orc` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the orthorhombic lattice. If
    the cell is not orthorhombic, the function will not work correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the orthorhombic conditions are satisfied.
    """

    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(c, ">", b, eps=length_tolerance) and compare_numerically(
        b, ">", a, eps=length_tolerance
    ):
        S = np.eye(3, dtype=float)
    elif compare_numerically(c, ">", a, eps=length_tolerance) and compare_numerically(
        a, ">", b, eps=length_tolerance
    ):
        S = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=float)
    elif compare_numerically(b, ">", c, eps=length_tolerance) and compare_numerically(
        c, ">", a, eps=length_tolerance
    ):
        S = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], dtype=float)
    elif compare_numerically(b, ">", a, eps=length_tolerance) and compare_numerically(
        a, ">", c, eps=length_tolerance
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(a, ">", c, eps=length_tolerance) and compare_numerically(
        c, ">", b, eps=length_tolerance
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(a, ">", b, eps=length_tolerance) and compare_numerically(
        b, ">", c, eps=length_tolerance
    ):
        S = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("orthorhombic")

    return S


def _ORCF_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary face-centered orthorhombic cell returns matrix S that transforms it to
    the standardized form.

    See :ref:`guide_orcf` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the face-centered orthorhombic
    lattice. If the cell is not face-centered orthorhombic, the function will not work
    correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the face-centered orthorhombic conditions are satisfied.
    """

    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(c, "<", b, eps=length_tolerance) and compare_numerically(
        b, "<", a, eps=length_tolerance
    ):
        S = np.eye(3, dtype=float)
    elif compare_numerically(c, "<", a, eps=length_tolerance) and compare_numerically(
        a, "<", b, eps=length_tolerance
    ):
        S = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=float)
    elif compare_numerically(b, "<", c, eps=length_tolerance) and compare_numerically(
        c, "<", a, eps=length_tolerance
    ):
        S = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], dtype=float)
    elif compare_numerically(b, "<", a, eps=length_tolerance) and compare_numerically(
        a, "<", c, eps=length_tolerance
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(a, "<", c, eps=length_tolerance) and compare_numerically(
        c, "<", b, eps=length_tolerance
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(a, "<", b, eps=length_tolerance) and compare_numerically(
        b, "<", c, eps=length_tolerance
    ):
        S = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("face-centered orthorhombic")

    return S


def _ORCI_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary body-centered orthorhombic cell returns matrix S that transforms it to
    the standardized form.

    See :ref:`guide_orci` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the body-centered orthorhombic
    lattice. If the cell is not body-centered orthorhombic, the function will not work
    correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the body-centered orthorhombic conditions are satisfied.
    """

    _, _, _, alpha, beta, gamma = get_params(cell)

    if compare_numerically(
        gamma, "<", beta, eps=angle_tolerance
    ) and compare_numerically(beta, "<", alpha, eps=angle_tolerance):
        S = np.eye(3, dtype=float)
    elif compare_numerically(
        gamma, "<", alpha, eps=angle_tolerance
    ) and compare_numerically(alpha, "<", beta, eps=angle_tolerance):
        S = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]], dtype=float)
    elif compare_numerically(
        beta, "<", gamma, eps=angle_tolerance
    ) and compare_numerically(gamma, "<", alpha, eps=angle_tolerance):
        S = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], dtype=float)
    elif compare_numerically(
        beta, "<", alpha, eps=angle_tolerance
    ) and compare_numerically(alpha, "<", gamma, eps=angle_tolerance):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif compare_numerically(
        alpha, "<", gamma, eps=angle_tolerance
    ) and compare_numerically(gamma, "<", beta, eps=angle_tolerance):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(
        alpha, "<", beta, eps=angle_tolerance
    ) and compare_numerically(beta, "<", gamma, eps=angle_tolerance):
        S = np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("body-centered orthorhombic")

    return S


def _ORCC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary base-centered orthorhombic cell returns matrix S that transforms it to
    the standardized form.

    See :ref:`guide_orcc` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the base-centered orthorhombic
    lattice. If the cell is not base-centered orthorhombic, the function will not work
    correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the base-centered orthorhombic conditions are satisfied.
    """

    _, _, _, alpha, beta, gamma = get_params(cell)

    if (
        compare_numerically(alpha, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, ">", 90.0, eps=angle_tolerance)
    ):
        S = np.eye(3, dtype=float)
    elif (
        compare_numerically(alpha, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "<", 90.0, eps=angle_tolerance)
    ):
        S = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    elif (
        compare_numerically(beta, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(alpha, ">", 90.0, eps=angle_tolerance)
    ):
        S = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif (
        compare_numerically(beta, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(alpha, "<", 90.0, eps=angle_tolerance)
    ):
        S = np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]], dtype=float)

    elif (
        compare_numerically(alpha, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, ">", 90.0, eps=angle_tolerance)
    ):
        S = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif (
        compare_numerically(alpha, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "<", 90.0, eps=angle_tolerance)
    ):
        S = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("base-centered orthorhombic")

    return S


def _HEX_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary hexagonal cell returns matrix S that transforms it to the standardized
    form.

    See :ref:`guide_hex` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the hexagonal lattice. If the
    cell is not hexagonal, the function will not work correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the hexagonal conditions are satisfied.
    """

    # Step 1
    _, _, _, alpha, beta, gamma = get_params(cell)

    if compare_numerically(
        alpha, "==", 90.0, eps=angle_tolerance
    ) and compare_numerically(beta, "==", 90.0, eps=angle_tolerance):
        S1 = np.eye(3, dtype=float)
    elif compare_numerically(
        beta, "==", 90.0, eps=angle_tolerance
    ) and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance):
        S1 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(
        alpha, "==", 90.0, eps=angle_tolerance
    ) and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance):
        S1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("hexagonal", step="first")

    # Step 2
    cell1 = S1.T @ cell
    _, _, _, _, _, gamma = get_params(cell)

    if compare_numerically(gamma, "==", 120.0, eps=angle_tolerance):
        S2 = np.eye(3, dtype=float)
    elif compare_numerically(gamma, "==", 60.0, eps=angle_tolerance):
        S2 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("hexagonal", step="second")

    return S1 @ S2


def _RHL_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary rhombohedral cell returns matrix S that transforms it to the standardized
    form.

    See :ref:`guide_rhl` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Completely ignored by this
        function, the arguments are defined only for the homogeneity of the input for all
        14 Bravais lattice types.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the rhombohedral lattice. If the
    cell is not rhombohedral, the function will not work correctly.
    """

    return np.eye(3, dtype=float)


def _MCL_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary monoclinic cell returns matrix S that transforms it to the standardized
    form.

    See :ref:`guide_mcl` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the monoclinic lattice. If the
    cell is not monoclinic, the function will not work correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the monoclinic conditions are satisfied.
    """

    # Step 1
    _, _, _, alpha, beta, gamma = get_params(cell)

    if (
        compare_numerically(beta, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(alpha, "!=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.eye(3, dtype=float)
    elif (
        compare_numerically(alpha, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "!=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif (
        compare_numerically(beta, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(alpha, "==", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "!=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("monoclinic", step="First")

    # Step 2
    cell1 = S1.T @ cell
    _, b, c, _, _, _ = get_params(cell1)

    if compare_numerically(b, "<=", c, eps=length_tolerance):
        S2 = np.eye(3, dtype=float)
    elif compare_numerically(b, ">", c, eps=length_tolerance):
        S2 = np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("monoclinic", step="Second")

    # Step 3
    cell2 = S2.T @ cell1
    _, _, _, alpha, _, _ = get_params(cell1)

    if compare_numerically(alpha, "<", 90.0, eps=angle_tolerance):
        S3 = np.eye(3, dtype=float)
    elif compare_numerically(alpha, ">", 90.0, eps=angle_tolerance):
        S3 = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("monoclinic", step="Third")

    return S1 @ S2 @ S3


def _MCLC_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary base-centered monoclinic cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_mclc` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the base-centered monoclinic
    lattice. If the cell is not base-centered monoclinic, the function will not work
    correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the base-centered monoclinic conditions are satisfied.
    """

    C = get_C_matrix("MCLC")

    # Step 1
    a, b, c, _, _, _ = get_params(cell)

    if compare_numerically(a, "==", b, eps=length_tolerance):
        S1 = np.eye(3, dtype=float)
    elif compare_numerically(b, "==", c, eps=length_tolerance):
        S1 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    elif compare_numerically(c, "==", a, eps=length_tolerance):
        S1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("base-centered monoclinic", step="First")

    # Step 2
    cell1 = S1.T @ cell
    cell1_c = C.T @ cell1
    _, b, c, _, _, _ = get_params(cell1_c)

    if compare_numerically(b, "<=", c, eps=length_tolerance):
        S2_c = np.eye(3, dtype=float)
    else:
        S2_c = np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=float)

    # Step 3
    cell2_c = S2_c.T @ cell1_c
    _, _, _, alpha, _, _ = get_params(cell2_c)

    if compare_numerically(alpha, "<", 90.0, eps=angle_tolerance):
        S3_c = np.eye(3, dtype=float)
    elif compare_numerically(alpha, ">", 90.0, eps=angle_tolerance):
        S3_c = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("base-centered monoclinic", step="Third")

    return S1 @ C @ S2_c @ S3_c @ np.linalg.inv(C)


def _TRI_get_S_matrix(cell, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    For arbitrary triclinic cell returns matrix S that transforms it to the
    standardized form.

    See :ref:`guide_tri` and :ref:`user-guide_conventions_which-cell_standardization` for
    details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors). Completely
        ignored by this function, the arguments are defined only for the homogeneity of
        the input for all 14 Bravais lattice types.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    Notes
    -----
    It is assumed that the ``cell`` has the symmetries of the triclinic lattice. If the
    cell is not triclinic, the function will not work correctly.

    Raises
    ------
    wulfric.exceptions.StandardizationTypeMismatch
        If none of the triclinic conditions are satisfied.
    """

    # Compute reciprocal cell
    rcell = get_reciprocal(cell)

    # Step 1
    _, _, _, alpha, beta, gamma = get_params(rcell)

    if (
        compare_numerically(alpha, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, ">=", 90.0, eps=angle_tolerance)
    ) or (
        compare_numerically(alpha, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "<=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.eye(3, dtype=float)
    elif (
        compare_numerically(alpha, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "<=", 90.0, eps=angle_tolerance)
    ) or (
        compare_numerically(alpha, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, ">=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    elif (
        compare_numerically(alpha, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, ">=", 90.0, eps=angle_tolerance)
    ) or (
        compare_numerically(alpha, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "<=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=float)
    elif (
        compare_numerically(alpha, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, ">=", 90.0, eps=angle_tolerance)
    ) or (
        compare_numerically(alpha, ">=", 90.0, eps=angle_tolerance)
        and compare_numerically(beta, "<=", 90.0, eps=angle_tolerance)
        and compare_numerically(gamma, "<=", 90.0, eps=angle_tolerance)
    ):
        S1 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=float)
    else:
        raise StandardizationTypeMismatch("triclinic", step="First")

    # Step 2
    rcell1 = S1.T @ rcell
    _, _, _, alpha, beta, gamma = get_params(rcell1)

    if (
        gamma == min(alpha, beta, gamma)
        and compare_numerically(gamma, ">=", 90.0, eps=angle_tolerance)
        or (
            gamma == max(alpha, beta, gamma)
            and compare_numerically(gamma, "<=", 90.0, eps=angle_tolerance)
        )
    ):
        S2 = np.eye(3, dtype=float)
    elif (
        beta == min(alpha, beta, gamma)
        and compare_numerically(beta, ">=", 90.0, eps=angle_tolerance)
        or (
            beta == max(alpha, beta, gamma)
            and compare_numerically(beta, "<=", 90.0, eps=angle_tolerance)
        )
    ):
        S2 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    elif (
        alpha == min(alpha, beta, gamma)
        and compare_numerically(alpha, ">=", 90.0, eps=angle_tolerance)
        or (
            alpha == max(alpha, beta, gamma)
            and compare_numerically(alpha, "<=", 90.0, eps=angle_tolerance)
        )
    ):
        S2 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
    else:
        raise StandardizationTypeMismatch("triclinic", step="Second")

    return np.linalg.inv(S1 @ S2).T


def get_S_matrix(cell, lattice_type=None, length_tolerance=1e-8, angle_tolerance=1e-4):
    r"""
    Computes standardization matrix :math:`\boldsymbol{S}` as defined in [1]_.

    See :ref:`docs for each Bravais lattice <user-guide_conventions_bravais-lattices>` for
    the details.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    lattice_type : str, optional
        One of the 14 lattice types that correspond to the provided ``cell``,
        case-insensitive. If not provided, then computed automatically from ``cell``. If
        provided, then it user's responsibility to ensure that ``lattice_type`` is
        correct.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).  Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    S : (3, 3) :numpy:`ndarray`
        Transformation matrix :math:`S`

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[3, 0, 0],[0, 1, 0],[0, 0, 2]]
        >>> wulf.cell.get_S_matrix(cell)
        array([[0., 0., 1.],
               [1., 0., 0.],
               [0., 1., 0.]])
    """
    cell = np.array(cell, dtype=float)

    if lattice_type is None:
        lattice_type = lepage(cell, angle_tolerance=angle_tolerance)

    lattice_type = lattice_type.upper()

    functions = {
        "CUB": _CUB_get_S_matrix,
        "FCC": _FCC_get_S_matrix,
        "BCC": _BCC_get_S_matrix,
        "TET": _TET_get_S_matrix,
        "BCT": _BCT_get_S_matrix,
        "ORC": _ORC_get_S_matrix,
        "ORCF": _ORCF_get_S_matrix,
        "ORCI": _ORCI_get_S_matrix,
        "ORCC": _ORCC_get_S_matrix,
        "HEX": _HEX_get_S_matrix,
        "RHL": _RHL_get_S_matrix,
        "MCL": _MCL_get_S_matrix,
        "MCLC": _MCLC_get_S_matrix,
        "TRI": _TRI_get_S_matrix,
    }

    return functions[lattice_type](
        cell, length_tolerance=length_tolerance, angle_tolerance=angle_tolerance
    )


def get_C_matrix(lattice_type):
    r"""
    Computes transformation matrix from standardized primitive to standardized
    conventional cell :math:`\boldsymbol{S}` as defined in [1]_.

    See :ref:`user-guide_conventions_which-cell_standardization` for details.

    Parameters
    ----------
    lattice_type : str
        One of the 14 lattice types. Case-insensitive.

    Returns
    -------
    C_matrix : (3, 3) :numpy:`ndarray`

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.get_C_matrix("ORCF")
        array([[-1.,  1.,  1.],
               [ 1., -1.,  1.],
               [ 1.,  1., -1.]])
    """

    return C_MATRICES[lattice_type.upper()]


def get_standardized(cell, S_matrix=None, length_tolerance=1e-8, angle_tolerance=1e-4):
    R"""
    Computes standardizes primitive cell as defined in [1]_.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    S_matrix : (3, 3) |array-like|_, optional
        Transformation matrix S. If not provided, then computed automatically from
        ``cell``. If provided, then it is user's responsibility to ensure that the matrix
        is the correct one for the given ``cell``.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).  Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    cell : (3, 3) :numpy:`ndarray`
        Standardized cell. Rows are interpreted as vectors. Independent from the initial
        cell, safe to modify.

        .. code-block:: python

            cell = [[a1_x, a1_y, a1_z],
                    [a2_x, a2_y, a2_z],
                    [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> cell = [[3, 0, 0],[0, 1, 0],[0, 0, 2]]
        >>> wulf.cell.get_standardized(cell)
        array([[0., 1., 0.],
               [0., 0., 2.],
               [3., 0., 0.]])
    """

    cell = np.array(cell, dtype=float)

    if S_matrix is None:
        lattice_type = lepage(cell, angle_tolerance=angle_tolerance)

        S_matrix = get_S_matrix(
            cell,
            lattice_type,
            length_tolerance=length_tolerance,
            angle_tolerance=angle_tolerance,
        )
    else:
        S_matrix = np.array(S_matrix, dtype=float)

    return S_matrix.T @ cell


def get_conventional(
    cell, S_matrix=None, C_matrix=None, length_tolerance=1e-8, angle_tolerance=1e-4
):
    r"""
    Computes standardizes conventional cell as defined in [1]_.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    S_matrix : (3, 3) |array-like|_, optional
        Transformation matrix S. If not provided, then computed automatically from
        ``cell``. If provided, then it is user's responsibility to ensure that the matrix
        is the correct one for the given ``cell``.
    C_matrix : (3, 3) |array-like|_, optional
        Transformation matrix C. If not provided, then computed automatically from
        ``cell``. If provided, then it is user's responsibility to ensure that the matrix
        is the correct one for the given ``cell``.
    length_tolerance : float, default :math:`10^{-8}`
        Tolerance for length variables (lengths of the lattice vectors).  Default value is
        chosen in the contexts of condense matter physics, assuming that length is given
        in Angstroms. Please choose appropriate tolerance for your problem.
    angle_tolerance : float, default :math:`10^{-4}`
        Tolerance for angle variables (angles of the lattice). Default value is chosen in
        the contexts of condense matter physics, assuming that angles are in degrees.
        Please choose appropriate tolerance for your problem.

    Returns
    -------
    conv_cell : (3, 3) :numpy:`ndarray`
        Conventional cell, rows are interpreted as vectors, columns - as coordinates.
        Independent from the initial cell, safe to modify.

        .. code-block:: python

            conv_cell = [[a1_x, a1_y, a1_z],
                         [a2_x, a2_y, a2_z],
                         [a3_x, a3_y, a3_z]]

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> orcf = wulf.cell.ORCF(a=1,b=2,c=3)
        >>> wulf.cell.get_conventional(orcf)
        array([[1., 0., 0.],
               [0., 2., 0.],
               [0., 0., 3.]])
    """
    cell = np.array(cell, dtype=float)

    if S_matrix is None or C_matrix is None:
        lattice_type = lepage(cell, angle_tolerance=angle_tolerance)

    if C_matrix is None:
        C_matrix = get_C_matrix(lattice_type)
    else:
        C_matrix = np.array(C_matrix, dtype=float)

    if S_matrix is None:
        S_matrix = get_S_matrix(
            cell,
            lattice_type,
            length_tolerance=length_tolerance,
            angle_tolerance=angle_tolerance,
        )
    else:
        S_matrix = np.array(S_matrix, dtype=float)

    return C_matrix.T @ S_matrix.T @ cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
