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

from wulfric.cell._lepage import lepage
from wulfric.cell._sc_standardize import get_S_matrix, get_standardized

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def standardize(
    cell, atoms, S_matrix=None, length_tolerance=1e-8, angle_tolerance=1e-4
):
    R"""
    Standardize cell with respect to the Bravais lattice type as defined in [1]_ and
    update atom's relative coordinates.

    Parameters
    ----------
    cell : (3, 3) |array-like|_
        Matrix of a primitive cell, rows are interpreted as vectors.
    atoms : dict
        Dictionary with atoms. Must have a ``"positions"`` with value of (N,3) |array-like|_.
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

    Notes
    -----

    ``atoms`` are not returned, but rather updated.

    References
    ----------
    .. [1] Setyawan, W. and Curtarolo, S., 2010.
        High-throughput electronic band structure calculations: Challenges and tools.
        Computational materials science, 49(2), pp. 299-312.

    Examples
    --------

    .. doctest::

        >>> import numpy as np
        >>> import wulfric as wulf
        >>> cell = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 3]])
        >>> atoms = {"names" : ["Cr1", "Cr2"], "positions" : [[0.7, 0, 0], [0, 0.2, 0]]}
        >>> atoms["positions"][0] @ cell, atoms["positions"][1] @ cell
        (array([1.4, 0. , 0. ]), array([0. , 0.2, 0. ]))
        >>> cell = wulf.crystal.standardize(cell, atoms)
        >>> cell
        array([[ 0., -1.,  0.],
               [-2.,  0.,  0.],
               [ 0.,  0., -3.]])
        >>> atoms
        {'names': ['Cr1', 'Cr2'], 'positions': [array([ 0. , -0.7,  0. ]), array([-0.2,  0. ,  0. ])]}
        >>> # Note that absolute coordinates of atoms are not changed.
        >>> atoms["positions"][0] @ cell, atoms["positions"][1] @ cell
        (array([1.4, 0. , 0. ]), array([0. , 0.2, 0. ]))

    """

    cell = np.array(cell, dtype=float)

    # Get S matrix before cell standardization
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

    # Standardize cell
    cell = get_standardized(cell=cell, S_matrix=S_matrix)

    # Recalculate atom's relative coordinates.
    atoms["positions"] = [
        np.linalg.inv(S_matrix) @ position for position in atoms["positions"]
    ]

    return cell


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
