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

from FreeCADGui import ViewProviderDocumentObject
from pivy import coin

from fpo import DisplayMode, proxy, view_proxy


# The ViewProxy is responsible for creating the display modes
@view_proxy()
class CustomSceneObjectVP:
    sphere = DisplayMode(name="Sphere", is_default=True)
    cube = DisplayMode(name="Cube")

    @sphere.builder
    def sphere_dm(self, _vo: ViewProviderDocumentObject) -> coin.SoSphere:
        self._sphere = coin.SoSphere()
        return self._sphere

    @cube.builder
    def cube_dm(self, _vo: ViewProviderDocumentObject) -> coin.SoCube:
        self._cube = coin.SoCube()
        return self._cube


# A Simple Data Proxy for demo
@proxy(view_proxy=CustomSceneObjectVP)
class CustomSceneObject:
    pass


# Use by just calling the create method from a macro or directly from the python
# console
def create_object():
    return CustomSceneObject.create(name="CustomViewModes")
