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


from wulfric.constants._sc_notation import BRAVAIS_LATTICE_NAMES, PEARSON_SYMBOLS

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def get_name(lattice_type):
    r"""
    Human-readable name of the Bravais lattice type.

    Parameters
    ----------
    lattice_type : str, optional
        One of the 14 lattice types. Case-insensitive.

    Returns
    -------
    name : str
        Name of the Bravais lattice type.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.get_name("CUB")
        'Cubic'
        >>> wulf.cell.get_name("MCLC")
        'C-centered monoclinic'
    """

    return BRAVAIS_LATTICE_NAMES[lattice_type.upper()]


def get_pearson_symbol(lattice_type):
    r"""
    Pearson symbol.

    Parameters
    ----------
    lattice_type : str, optional
        One of the 14 lattice types. Case-insensitive.

    Returns
    -------
    pearson_symbol : str
        Pearson symbol of the lattice.

    Notes
    -----
    See: |PearsonSymbol|_

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.get_pearson_symbol("CUB")
        'cP'
        >>> wulf.cell.get_pearson_symbol("MCLC")
        'mS'
        >>> wulf.cell.get_pearson_symbol("Tri")
        'aP'
        >>> wulf.cell.get_pearson_symbol("ORCC")
        'oS'
    """

    return PEARSON_SYMBOLS[lattice_type.upper()]


def get_crystal_family(lattice_type):
    r"""
    Crystal family.

    Parameters
    ----------
    lattice_type : str, optional
        One of the 14 lattice types. Case-insensitive.

    Returns
    -------
    crystal_family : str
        Crystal family of the lattice.

    Notes
    -----
    See: |PearsonSymbol|_

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.get_crystal_family("CUB")
        'c'
        >>> wulf.cell.get_crystal_family("MCLC")
        'm'
        >>> wulf.cell.get_crystal_family("Tri")
        'a'
        >>> wulf.cell.get_crystal_family("ORCC")
        'o'
    """

    return PEARSON_SYMBOLS[lattice_type.upper()][0]


def get_centring_type(lattice_type):
    r"""
    Centring type.

    Parameters
    ----------
    lattice_type : str, optional
        One of the 14 lattice types. Case-insensitive.

    Returns
    -------
    centring_type : str
        Centring type of the lattice.

    Notes
    -----
    See: |PearsonSymbol|_



    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> wulf.cell.get_centring_type("CUB")
        'P'
        >>> wulf.cell.get_centring_type("MCLC")
        'S'
        >>> wulf.cell.get_centring_type("Tri")
        'P'
        >>> wulf.cell.get_centring_type("ORCC")
        'S'
    """

    return PEARSON_SYMBOLS[lattice_type.upper()][1]


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
