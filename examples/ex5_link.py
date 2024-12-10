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

# ruff: noqa: D401, ERA001

from fpo import (
    PropertyBool,
    PropertyInteger,
    PropertyLink,
    PropertyPlacement,
    events,
    get_selection,
    print_err,
    proxy,
)


# This class has the basic stuff to behave lik a Link Object
# See: https://github.com/realthunder/FreeCAD_assembly3/wiki/Link#app-namespace
# The most important part is to add the extension: App::LinkExtensionPython
#
@proxy(extensions=["App::LinkExtensionPython"])
class CustomLinkArray:

    # Define the important linked properties
    source_object = PropertyLink(name="SourceObject", section="Link", link_property="LinkedObject")
    placement = PropertyPlacement(name="Placement", section="Link", link_property=True)
    show_element = PropertyBool(name="ShowElement", section="Array", link_property=True)
    element_count = PropertyInteger(name="ElementCount", section="Array", link_property=True)

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


# Use it by selecting an object and calling this function from a macro or
# directly from the python console
#
#  import ex5_link as ln
#  ln.create_link()
#
def create_link(count: int = 0):
    # Pick one object of any type from the current selection
    ok, obj = get_selection("*")
    if ok:
        # Create your ScriptedObject
        link = CustomLinkArray.create("CustomArray")
        # Set the link target
        link.SourceObject = obj
        # Set the count if you want an array
        if count:
            link.ElementCount = count
        return link

    print_err("There are no objects selected.")
    return None
