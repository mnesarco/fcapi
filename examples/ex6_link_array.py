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

# ruff: noqa: D401, ERA001, N806

import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Placement, Rotation, Vector

from fpo import (
    PropertyAngle,
    PropertyBool,
    PropertyInteger,
    PropertyLink,
    PropertyOptions,
    PropertyPlacement,
    events,
    get_selection,
    message_box,
    proxy,
    set_immutable_prop,
)


# Options for links arrangement
def array_steps_options():
    return ["Full Circle", "Interval"]


# This class has the basic stuff to behave lik a Link Object
# See: https://github.com/realthunder/FreeCAD_assembly3/wiki/Link#app-namespace
# The most important part is to add the extension: App::LinkExtensionPython
#
@proxy(extensions=["App::LinkExtensionPython"])
class CustomCircularArray:

    # Define the important linked properties
    source_object = PropertyLink(name="SourceObject", section="Link", link_property="LinkedObject")
    placement = PropertyPlacement(name="Placement", section="Link", link_property=True)
    show_element = PropertyBool(name="ShowElement", section="Array", link_property=True)
    element_count = PropertyInteger(name="ElementCount", section="Array", link_property=True)

    # Properties for circular array logic
    axis = PropertyLink(name="Axis", section="Array")
    full_angle = PropertyAngle(name="FullAngle", section="Array")
    interval_angle = PropertyAngle(name="IntervalAngle", section="Array")
    array_steps = PropertyOptions(name="ArraySteps", section="Array",
                                  options_provider=array_steps_options)

    # Some obscure Link required thing
    @show_element.observer
    def show_element_change(self, e: events.PropertyChangedEvent):
        """Required to support link array."""
        if hasattr(e.source, "PlacementList"):
            # this allows to move individual elements by the user
            if e.new_value:
                e.source.setPropertyStatus("PlacementList", "-Immutable")
            else:
                e.source.setPropertyStatus("PlacementList", "Immutable")

    # Prevent invalid element_count for the array case
    @element_count.observer
    def element_count_change(self, e: events.PropertyChangedEvent):
        """Number of elements in the array (including the original)."""
        if e.new_value < 1:
            self.element_count = 1

    # Do the magic
    def on_execute(self):

        # Validate inputs
        if not self.source_object or not self.axis:
            return

        # Calculate angles depending on selected option

        if self.array_steps == "Interval":
            self.full_angle = (self.element_count-1) * self.interval_angle

        elif  self.array_steps == "Full Circle":
            self.full_angle = 360
            self.interval_angle = self.full_angle / self.element_count

        # Generate Placements
        source = self.source_object
        placements = []
        for i in range(self.element_count):
            rot_i = Rotation(Vector(0,0,1), i * self.interval_angle)
            pla_i = Placement(Vector(0,0,0), rot_i)
            placement = self.axis.Placement * pla_i * self.axis.Placement.inverse() * source.Placement
            placements.append(placement)

        # Update placements (Link api)
        set_immutable_prop(self.Object, "PlacementList", placements)



# Use it by selecting an axis and an object and calling this function from a macro or
# directly from the python console
#
#  import ex6_link_array as ln
#  ln.create_circular_array(6)
#
def create_circular_array(count: int = 0):
    # Get valid selection: an axis and an object
    # The supported Axis is a PartDesign datum line
    ok, selAxis, selObj = get_selection("PartDesign::Line", "*")

    # Validate inputs
    if not ok:
        msg = "Please select an object and an axis belonging to the same part"
        message_box(msg)
        return None

    # check that object and axis belong to the same parent
    objParent = selObj.getParentGeoFeatureGroup()
    axisParent = selAxis.getParentGeoFeatureGroup()
    if objParent != axisParent:
        msg = "Please select an object and an axis belonging to the same part"
        message_box(msg)
        return None

    # Create the Link Array
    array = CustomCircularArray.create(selObj.Name + "_Array")
    array.SourceObject = selObj
    array.Axis = selAxis
    array.ArraySteps = "Full Circle"
    array.ElementCount = 6
    # hide original object
    array.SourceObject.ViewObject.hide()
    # update
    array.recompute()
    objParent.recompute()
    App.ActiveDocument.recompute()
    Gui.Selection.clearSelection()

    if count:
        array.ElementCount = count

    return array
