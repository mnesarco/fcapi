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
from fpo import PropertyLength, get_pd_active_body, print_err, proxy, set_pd_shape


# Here we will create a simple Cube with PartDesign semantic
#
@proxy(
    object_type="PartDesign::FeatureAdditivePython",
    extensions=["Part::AttachExtensionPython"])
class PDMyCubeAdd:
    length = PropertyLength(default=10)
    width = PropertyLength(default=10)
    height = PropertyLength(default=10)

    # Ensure execution by the first time
    def on_create(self, obj):
        self.on_execute(obj)

    # Update the shape
    def on_execute(self, obj):
        cube = Part.makeBox(self.length, self.width, self.height)
        set_pd_shape(obj, cube)


# Use by just calling the create method from a macro or directly from the python
# console
def create_cube_pd():
    body = get_pd_active_body()
    if not body:
        print_err("No active body.")
        return

    cube = PDMyCubeAdd.create(name="CubeFeature")
    body.addObject(cube)
