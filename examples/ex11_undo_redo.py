#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
#  (c) 2024 Frank David Martínez Muñoz.
#

# ruff: noqa: D401, ERA001, N806, ANN201, D102, D101, D103

# Lets reuse one existing example to to demonstrate undo/redo transactions
import ex2_cube as cube

from fpo import transaction

# Lets create one cube in one transaction
with transaction("One Cube"):
    cube.create_cube("FirstCube")

# Now lets create 3 cubes in one transaction
with transaction("Three Cubes"):
    cube.create_cube("Cube1")
    cube.create_cube("Cube2")
    cube.create_cube("Cube3")

# Now you can play with Ctrl+Z (undo), Ctrl+Shift+Z (redo)

# -----

# Aborting a transaction in the middle intentionally
with transaction("Cancel something") as tx:
    for i in range(5):
        cube.create_cube(f"BadCube{i}")
        if i == 3:  # noqa: PLR2004
            tx.abort()

# -----

# Recovering from an unexpected error
with transaction("Bad day"):
    for i in range(5):
        cube.create_cube(f"BadCube{i}")
        if i == 3:  # noqa: PLR2004
            msg = "Something goes wrong"
            raise RuntimeError(msg)
