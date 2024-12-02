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

from fpo import proxy, view_proxy

# ViewProvider with GroupBehavior
@view_proxy(icon="self:group.svg")
class MyGroupViewProxy:
    pass


# Proxy with GroupBehavior
@proxy(
    object_type="App::DocumentObjectGroupPython", # <-----
    view_proxy=MyGroupViewProxy,
)
class MyGroupProxy:
    pass

# Use by just calling the create method from a macro or directly from the python
# console
def create_group():
    return MyGroupProxy.create(name="MyDocGroup")
