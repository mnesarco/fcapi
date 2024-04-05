# -*- coding: utf-8 -*-
#
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

from fpo import proxy, view_proxy, PropertyInteger, DisplayMode


# ViewProviders allows to control presentation things like the Icon of the
# Object in the Tree
@view_proxy(icon='self:compass-drafting-solid.svg')
class MyDataObjView:
    pass


# The most basic `ScriptedObject` is one with a bunch of properties, it can be used
# in replacement of a Spreadsheet as all the properties support expressions.
#
@proxy(view_proxy=MyDataObjView)
class MyDataObj:
    whatever = PropertyInteger(default=3)


# Use by just calling the create method from a macro or directly from the python
# console
def create_data():
    return MyDataObj.create(name="Params")

