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

# Port of https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/PartDesign/Scripts/Spring.py
# Copyright of the original file: (c) 2011 Adrian Przekwas LGPL

import Part
from fpo import proxy, PropertyLength


@proxy(object_type="Part::FeaturePython")
class MySpring2:

   pitch = PropertyLength(default=5.0, description="Pitch of the helix")
   diameter = PropertyLength(default=6.0, description="Diameter of the helix")
   height = PropertyLength(default=30.0, description="Height of the helix")
   bar_diameter = PropertyLength(default=3.0, description="Diameter of the bar")

   def on_execute(self, obj):
      my_helix = Part.makeHelix(self.pitch, self.height, self.diameter/2)
      g = my_helix.Edges[0].Curve
      c = Part.Circle()
      c.Center = g.value(0)  # start point of the helix
      c.Axis = (0, 1, 0)
      c.Radius = self.bar_diameter/2
      section = Part.Wire([c.toShape()])
      make_solid = True
      is_frenet = True
      obj.Shape = Part.Wire(my_helix).makePipeShell([section], make_solid, is_frenet)

   def on_create(self, obj):
      self.on_execute(obj)


# Use by just calling the create method from a macro or directly from the python
# console
def create_spring():
   MySpring2.create(label="My Spring")
