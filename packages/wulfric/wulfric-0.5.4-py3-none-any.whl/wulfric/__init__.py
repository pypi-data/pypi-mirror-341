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


__version__ = "0.5.4"
__doclink__ = "wulfric.org"
__git_hash__ = "285d1a35e948c977ed506e4ae3a51f3b451a82a1"
__release_date__ = "14 April 2025"


from . import cell, constants, crystal, geometry, io, visualization
from ._decorate_array import *
from ._exceptions import *
from ._kpoints_class import *
from ._numerical import *
from ._package_info import *
from ._syntax_sugar import *
