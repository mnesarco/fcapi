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

"""
Code layout reflects Gui layout.

Dialog
  └── Col (Vertical Layout)
      └── InputInt
      └── InputBoolean
      └── InputText
      └── button
"""

# ruff: noqa: SIM117

#codeblock
import fcui as ui

with ui.Dialog("Basic Form") as form:
    with ui.Col():
        var1 = ui.InputInt(label="Some int:")
        var2 = ui.InputBoolean(label="Some Boolean")
        var3 = ui.InputText(label="Some Text")

        @ui.button(label="Do something")
        def something() -> None:
            """Execute on click."""
            ui.print_log(f"{var1.value()=}, {var2.value()=}, {var3.value()=}")
#/codeblock
