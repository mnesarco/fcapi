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

import Part

from fpo import PropertyLength, proxy


# The most basic `ScriptedObject` with a shape is a cube or box.
# As we need a Shape, we will use Part::FeaturePython object type instead of
# the default App::FeaturePython
#
@proxy(object_type="Part::FeaturePython")
class MyCube:
    length = PropertyLength(default=10)
    width = PropertyLength(default=10)
    height = PropertyLength(default=10)

    # Ensure execution by the first time
    def on_create(self):
        self.on_execute()

    # Update the shape
    def on_execute(self):
        self.Object.Shape = Part.makeBox(self.length, self.width, self.height)


# Use by just calling the create method from a macro or directly from the python
# console
def create_cube(name: str = "Cube"):
    return MyCube.create(name=name)
