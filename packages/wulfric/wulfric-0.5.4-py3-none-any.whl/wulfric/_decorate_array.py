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
from termcolor import colored

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def print_2d_array(
    array,
    fmt=">.2f",
    highlight=False,
    print_result=True,
    borders=True,
    shift=0,
    header_row=None,
    footer_row=None,
    header_column=None,
    footer_column=None,
):
    r"""
    Decorates 1D and 2D arrays.

    Parameters
    ----------
    array : (N,) or (N, M) |array-like|_
        Array to be decorated.
    fmt : str, default ">.2f"
        Format string.
    highlight : bool, default False
        Whether to highlight positive and negative values.
        Only works for real-valued arrays.
    print_result : bool, default True
        Whether to print the result or return it as a string.
    borders : bool, default True
        Whether to print borders around the array.
    shift : int, default 0
        Shifts the array to the right by ``shift`` columns.
    header_row : list, optional
        Header of the table (top). Has to have the same length as the number of columns.
        Has to had one more element for each if ``header_column`` or ``footer_column`` is not None.
    footer_row : list, optional
        Footer of the table (bottom). Has to have the same length as the number of columns.
        Has to had one more element for each if ``header_column`` or ``footer_column`` is not None.
    header_column : list, optional
        Header of the table (left). Has to have the same length as the number of rows.
    footer_column : list, optional
        Footer of the table (right). Has to have the same length as the number of rows.

    Returns
    -------
    string : str
        String representation of the array.
        Returned only if ``print_result`` is False.

    Examples
    --------

    .. doctest::

        >>> import wulfric as wulf
        >>> array = [[1, 2], [3, 4], [5, 6]]
        >>> wulf.print_2d_array(array)
        ┌──────┬──────┐
        │ 1.00 │ 2.00 │
        ├──────┼──────┤
        │ 3.00 │ 4.00 │
        ├──────┼──────┤
        │ 5.00 │ 6.00 │
        └──────┴──────┘
        >>> wulf.print_2d_array(array, header_column=["a", "B", "c"], header_row = ["", "A", "B"])
        ┌───┬──────┬──────┐
        │   │    A │    B │
        ├───┼──────┼──────┤
        │ a │ 1.00 │ 2.00 │
        ├───┼──────┼──────┤
        │ B │ 3.00 │ 4.00 │
        ├───┼──────┼──────┤
        │ c │ 5.00 │ 6.00 │
        └───┴──────┴──────┘
        >>> array[1][1] = None
        >>> wulf.print_2d_array(array)
        ┌──────┬──────┐
        │ 1.00 │ 2.00 │
        ├──────┼──────┤
        │ 3.00 │      │
        ├──────┼──────┤
        │ 5.00 │ 6.00 │
        └──────┴──────┘
        >>> array = [[1, 2 + 1j], [3, 4], [52, 6]]
        >>> wulf.print_2d_array(array)
        ┌───────┬──────────────┐
        │  1.00 │ 2.00 + i1.00 │
        ├───────┼──────────────┤
        │  3.00 │ 4.00         │
        ├───────┼──────────────┤
        │ 52.00 │ 6.00         │
        └───────┴──────────────┘
    """

    top_border = ("┌", "┬", "┐")
    middle_border = ("├", "┼", "┤")
    bottom_border = ("└", "┴", "┘")
    if borders:
        vert = "│"
        space_vert = f" {vert}"
    else:
        vert = ""
        space_vert = ""

    array = np.array(array)
    if (len(array.shape) == 1 and array.shape[0] != 0) or (
        len(array.shape) == 2 and array.shape[1] != 0
    ):
        # Convert 1D array to 2D array
        if len(array.shape) == 1:
            array = np.array([array])

        # Array dimensions
        N = len(array)
        M = len(array[0])

        # Check if header_row, footer_row, header_column and footer_column have the correct length
        if header_column is not None and len(header_column) != N:
            raise ValueError(
                f"header_column has to have the same length"
                + f" as the number of rows ({N})."
                + f"It has length of {len(header_column)}. "
            )
        if footer_column is not None and len(footer_column) != N:
            raise ValueError(
                f"footer_column has to have the same length"
                + f" as the number of rows ({N})."
                + f"It has length of {len(footer_column)}. "
            )
        if header_row is not None and len(header_row) != M + int(
            header_column is not None
        ) + int(footer_column is not None):
            raise ValueError(
                f"header_row has to have the same length "
                + f"({M + int(header_column is not None) + int(footer_column is not None)})"
                + f" as the number of columns ({M}) + one more element for each if "
                + "header_column or footer_column is not None "
                + f"(+{int(header_column is not None) + int(footer_column is not None)}). "
                + f"It has length of {len(header_row)}."
            )
        if footer_row is not None and len(footer_row) != M + int(
            header_column is not None
        ) + int(footer_column is not None):
            raise ValueError(
                f"footer_row has to have the same length "
                + f"({M + int(header_column is not None) + int(footer_column is not None)})"
                + f" as the number of columns ({M}) + one more element for each if "
                + "header_column or footer_column is not None "
                + f"(+{int(header_column is not None) + int(footer_column is not None)}). "
                + f"It has length of {len(footer_row)}."
            )

        # Fix RAD-tools:issue#3
        array[array == 0] = 0

        # Define functions for printing numbers and borders
        def print_number(number, fmt, highlight=False, condition=None):
            if condition is None:
                condition = number
            string = ""
            if number is None:
                return " " * len(f"{1:{fmt}}")
            # Highlight positive and negative values with colours
            if highlight:
                if condition > 0:
                    string += colored(f"{number:{fmt}}", "red", attrs=["bold"])
                elif condition < 0:
                    string += colored(f"{number:{fmt}}", "blue", attrs=["bold"])
                else:
                    string += colored(f"{number:{fmt}}", "green", attrs=["bold"])
            # Print without colours
            else:
                string += f"{number:{fmt}}"
            return string

        def print_complex(number, fmt, highlight=False):
            string = ""
            if number.real != 0:
                string += print_number(number.real, fmt, highlight)
            else:
                string += " " * len(print_number(number.real, fmt))

            if number.imag > 0:
                sign = "+"
            else:
                sign = "-"

            if number.imag != 0:
                string += f" {sign} i"
                string += print_number(
                    abs(number.imag), f"<{fmt}", highlight, condition=number.imag
                )
            else:
                string += " " * (
                    len(print_number(abs(number.imag), fmt, condition=number.imag)) + 4
                )
            return string

        def print_border(symbol_start, symbol_middle, symbol_end, n):
            result = [symbol_start]
            if header_column is not None:
                result.append(f"{(n[0]+2)*'─'}{symbol_middle}")
                n_index_shift = 1
            else:
                n_index_shift = 0
            for j in range(0, M):
                # If at least one complex value is present in the column
                if np.iscomplex(array[:, j]).any():
                    result.append(f"{(2*n[j + n_index_shift] + 6)*'─'}")
                else:
                    result.append(f"{(n[j + n_index_shift] + 2)*'─'}")
                if j != M - 1 or footer_column is not None:
                    result.append(symbol_middle)

            if footer_column is not None:
                result.append(f"{(n[-1]+2)*'─'}")
            result.append(f"{symbol_end}\n")
            return "".join(result)

        # Get maximum string length for each column of an array
        n = np.zeros(M, dtype=int)
        n_full = np.zeros(M, dtype=int)
        for column in range(M):
            for row in range(N):
                if array[row][column] is None or np.isnan(array[row][column]):
                    pass
                elif np.iscomplex(array[row, column]):
                    n[column] = max(
                        n[column], (len(print_complex(array[row][column], fmt)) - 4) / 2
                    )
                    n_full[column] = max(
                        n_full[column], len(print_complex(array[row][column], fmt))
                    )
                else:
                    n[column] = max(
                        n[column], len(print_number(array[row][column].real, fmt))
                    )

        # Parse fmt
        tmp_fmt, post_fmt = fmt.split(".")
        mid_fmt = "".join(c for c in tmp_fmt if c.isdigit())
        pre_fmt = "".join(c for c in tmp_fmt if not c.isdigit())

        # Force provided fmt
        if len(mid_fmt) != 0:
            n = np.amax([n, [int(mid_fmt) for _ in n]], axis=0)

        # Get format for headers and footers
        if header_column is not None:
            tmp_n = max([len(str(x)) for x in header_column])
            n = np.concatenate(([tmp_n], n))
            n_full = np.concatenate(([tmp_n], n_full))
        if footer_column is not None:
            tmp_n = max([len(str(x)) for x in footer_column])
            n = np.concatenate((n, [tmp_n]))
            n_full = np.concatenate((n_full, [tmp_n]))
        if header_row is not None:
            n = np.amax([n, [len(str(x)) for x in header_row]], axis=0)
        if footer_row is not None:
            n = np.amax([n, [len(str(x)) for x in footer_row]], axis=0)

        n_full = np.amax([n, n_full], axis=0)

        string = []
        # Open borders
        if borders:
            string.append(" " * shift + print_border(*top_border, n))
        # Write header row
        if header_row is not None:
            string.append(" " * shift + vert)
            string.extend(
                [
                    f" {x:{pre_fmt}{n_full[x_i]}}{space_vert}"
                    for x_i, x in enumerate(header_row)
                ]
            )
            string.append("\n")
            if borders:
                string.append(" " * shift + print_border(*middle_border, n))

        # Write array
        for i in range(0, N):
            substring = [" " * shift, vert]
            if header_column is not None:
                substring.append(f" {header_column[i]:{pre_fmt}{n[0]}}{space_vert}")
                n_index_shift = 1
            else:
                n_index_shift = 0

            for j in range(0, M):
                fmt = f"{pre_fmt}{n[j + n_index_shift]}.{post_fmt}"
                substring.append(" ")
                # Print blank for None
                if array[i][j] is None or np.isnan(array[i][j]):
                    # Highlight positive and negative values with colours
                    substring.append(
                        " " * (len(f"{'':{pre_fmt}{n[j + n_index_shift]}}"))
                    )
                # Print complex values
                elif np.iscomplex(array[:, j]).any():
                    # Print complex part if it is non-zero
                    substring.append(print_complex(array[i][j], fmt, highlight))
                # Print real values
                else:
                    # Highlight positive and negative values with colours
                    substring.append(print_number(array[i][j].real, fmt, highlight))
                substring.append(space_vert)

            if footer_column is not None:
                substring.append(f" {footer_column[i]:{pre_fmt}{n[-1]}}{space_vert}")

            substring.append("\n")

            if borders and i != N - 1:
                # Middle of the table
                substring.append(" " * shift + print_border(*middle_border, n))

            string.extend(substring)

        # Write footer row
        if footer_row is not None:
            if borders:
                string.append(" " * shift + print_border(*middle_border, n))
            string.append(" " * shift + vert)
            string.extend(
                [
                    f" {x:{pre_fmt}{n_full[x_i]}}{space_vert}"
                    for x_i, x in enumerate(footer_row)
                ]
            )
            string.append("\n")
        # Close borders
        if borders:
            string.append(" " * shift + print_border(*bottom_border, n))

        # Print or return result
        string = "".join(string)
        if string[-1] == "\n":
            string = string[:-1]
        if print_result:
            print(string)
        else:
            return string
    else:
        if print_result:
            print(None)
        else:
            return None


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
