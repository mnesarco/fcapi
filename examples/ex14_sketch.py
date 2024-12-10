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

import FreeCAD as App
import Part

import fpo

# Custom Sketch object that autogenerates circles in a line


@fpo.proxy(object_type="Sketcher::SketchObjectPython")  # <----
class AlignedCircles:

    count = fpo.PropertyInteger(default=3, description="Number of circles")
    spacing = fpo.PropertyFloat(default=20, description="Spacing between centers")
    diameter = fpo.PropertyFloat(default=10, description="Diameter of all circles")

    def on_execute(self):
        sketch = self.Object
        sketch.deleteAllGeometry()
        radius = self.diameter / 2.0
        for i in range(self.count):
            y_position = i * self.spacing
            shape = Part.Circle(App.Vector(0, y_position, 0), App.Vector(0, 0, 1), radius)
            sketch.addGeometry(shape, False)
        sketch.recompute()


def create_sketch():
    AlignedCircles.create(name="MyAlignedCircles")
