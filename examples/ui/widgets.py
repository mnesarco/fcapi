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

from pathlib import Path
import fcui as ui
import importlib as imp
import FreeCAD as App
from PySide.QtCore import Qt, QRect
from PySide.QtGui import QIcon, QWidget, QPainter

imp.reload(ui)

#codeblock InputFloatList
def demo_InputFloatList():
    with ui.Dialog("InputFloatList"):
        with ui.Col():
            val = ui.InputFloatList(
                values=[1.0, 2.0, 3.2, 10.5],
                label="Some floats:",
                resizable=True,
            )

            @ui.button("Print")
            def btn_print():
                ui.print_log(val.value())
#/codeblock


#codeblock Dialog
def demo_Dialog():
    with ui.Dialog("Dialog"):
        with ui.Col():
            ui.TextLabel("This a simple text", alignment=Qt.AlignCenter)
#/codeblock


#codeblock Scroll
def demo_Scroll():
    with ui.Dialog("Scroll"):
        with ui.Scroll(widgetResizable=True):
            with ui.Container():
                _v1 = ui.InputVector(label="Input vector:")
                _v2 = ui.InputVector(label="Input vector:")
#/codeblock


#codeblock GroupBox
def demo_GroupBox():
    with ui.Dialog("GroupBox"):
        with ui.GroupBox("General"):
            _quant = ui.InputInt(label="Quantity:")
            _round = ui.InputBoolean(label="Round:")
        with ui.GroupBox("Details"):
            _desc = ui.InputText(label="Description:")
            _rate = ui.InputFloat(label="Rate:")
#/codeblock


#codeblock TabContainer
def demo_TabContainer():
    with ui.Dialog("TabContainer"):
        with ui.TabContainer():
            with ui.Tab("General"):
                _quant = ui.InputInt(label="Quantity:")
                _round = ui.InputBoolean(label="Round:")
            with ui.Tab("Details"):
                _desc = ui.InputText(label="Description:")
                _rate = ui.InputFloat(label="Rate:")
#/codeblock


#codeblock Splitter
def demo_Splitter():
    with ui.Dialog("Splitter"):
        with ui.Splitter():
            with ui.Container():
                _quant = ui.InputInt(label="Quantity:")
                _round = ui.InputBoolean(label="Round:")
            with ui.Container():
                _desc = ui.InputText(label="Description:")
                _rate = ui.InputFloat(label="Rate:")
#/codeblock


#codeblock Col
def demo_Col():
    with ui.Dialog("Col"):
        with ui.Col():
            ui.TextLabel("Number:", alignment=Qt.AlignCenter)
            ui.InputInt(alignment=Qt.AlignCenter)
            ui.TextLabel("Boolean:", alignment=Qt.AlignCenter)
            ui.InputBoolean(alignment=Qt.AlignCenter)
            ui.TextLabel("Text:", alignment=Qt.AlignCenter)
            ui.InputText(alignment=Qt.AlignCenter)
            ui.TextLabel("Float:", alignment=Qt.AlignCenter)
            ui.InputFloat(alignment=Qt.AlignCenter)
#/codeblock


#codeblock Row
def demo_Row():
    with ui.Dialog("Row"):
        with ui.Row():
            ui.TextLabel("Number:")
            ui.InputInt()
            ui.TextLabel("Boolean:")
            ui.InputBoolean()
            ui.TextLabel("Text:")
            ui.InputText()
            ui.TextLabel("Float:")
            ui.InputFloat()
#/codeblock



#codeblock InputVector
def demo_InputVector():
    with ui.Dialog("InputVector"):
        with ui.Col():
            val = ui.InputVector(label="Input vector:")

            @ui.button("Print")
            def btn_print():
                ui.print_log(val.value())
#/codeblock


#codeblock Html
def demo_Html():
    with ui.Dialog("Html"):
        with ui.Col():
            ui.Html(
                background="#ffffff",
                html="""
                <h1>Header</h1>
                <ul>
                    <li>Item 1</li>
                    <li>Item 1</li>
                    <li>Item 1</li>
                </ul>
                <br />
                <p>
                <strong>Be Happy!!</strong>
                </p>
                """
            )
#/codeblock


#codeblock TextLabel
def demo_TextLabel():
    with ui.Dialog("TextLabel"):
        with ui.Col():
            ui.TextLabel("This is a text label", alignment=Qt.AlignCenter)
#/codeblock


#codeblock InputBoolean
def demo_InputBoolean():
    with ui.Dialog("InputBoolean"):
        val = ui.InputBoolean(label="Are you ok?:", alignment=Qt.AlignCenter)

        @ui.button("Print")
        def btn_print():
            ui.print_log(val.value())
#/codeblock


#codeblock InputFloat
def demo_InputFloat():
    with ui.Dialog("InputFloat"):
        val = ui.InputFloat(value=5.0, label="Enter is a float:", alignment=Qt.AlignCenter)

        @ui.button("Print")
        def print_float():
            ui.print_log(val.value())
#/codeblock


#codeblock InputText
def demo_InputText():
    with ui.Dialog("InputText"):
        text = ui.InputText(value="Hello World", label="Some text:", alignment=Qt.AlignCenter)

        @ui.button("Print")
        def print_text():
            ui.print_log(text.value())
#/codeblock


#codeblock InputQuantity
def demo_InputQuantity():
    App.activeDocument().addObject("Part::Box", "Box1")
    with ui.Dialog("InputQuantity"):
        quantity = ui.InputQuantity(
            label="Length:",
            obj=App.activeDocument().getObject("Box1"),
            property="Length",
            unit="in",
            alignment=Qt.AlignCenter,
        )

        quantity2 = ui.InputQuantity(
            value=5.0, label="Length Free:", unit="in", alignment=Qt.AlignCenter
        )

        @ui.button("Print")
        def print_q():
            ui.print_log(quantity.value(), quantity2.value())
#/codeblock


#codeblock InputInt
def demo_InputInt():
    with ui.Dialog("InputInt"):
        val = ui.InputInt(value=5, label="Enter is an int:", alignment=Qt.AlignCenter)

        @ui.button("Print")
        def print_int():
            ui.print_log(val.value())
#/codeblock


#codeblock InputOptions
def demo_InputOptions():
    with ui.Dialog("InputOptions"):
        val = ui.InputOptions(
            options={
                "First": 10,
                "Second": 20,
                "Third": 30,
            },
            value=20,
            label="Select an option:",
            alignment=Qt.AlignCenter,
        )

        @ui.button("Print")
        def print_opt():
            ui.print_log(val.value())
#/codeblock


#codeblock InputSelectOne
def demo_InputSelectOne():
    with ui.Dialog("InputSelectOne", modal=False):
        val = ui.InputSelectOne(label="Pick one object from the 3D view:")

        @ui.button("Print")
        def print_sel():
            ui.print_log(val.value())
#/codeblock


#codeblock InputSelectMany
def demo_InputSelectMany():
    with ui.Dialog("InputSelectMany", modal=False):
        val = ui.InputSelectMany(label="Pick one or more objects from the 3D view:")

        @ui.button("Print")
        def print_sel():
            ui.print_log(val.value())
#/codeblock


#codeblock buttons
def demo_buttons():
    with ui.Dialog("Buttons", modal=False):

        @ui.button("Button")
        def btn1():
            ui.print_log("Hello btn1")

        @ui.button("Tool Button", tool=True)
        def btn2():
            ui.print_log("Hello btn2")

        @ui.button("Button with icon and text", icon=QIcon(":icons/Std_ViewHome.svg"))
        def btn3():
            ui.print_log("Hello btn3")

        @ui.button(icon=QIcon(":icons/zoom-in.svg"))
        def btn4():
            ui.print_log("Hello btn4")

        @ui.button(icon=QIcon(":icons/zoom-out.svg"), tool=True)
        def btn5():
            ui.print_log("Hello btn4")
#/codeblock

#codeblock ImageView
def demo_ImageView():
    with ui.Dialog("ImageView", size=(400, 300)):
        with ui.Col():
            ui.ImageView(
                str(Path(__file__).parent / 'image.png')
            )
#/codeblock


#codeblock SvgImageView
def demo_SvgImageView():
    with ui.Dialog("SvgImageView"):
        with ui.Col():
            ui.SvgImageView(
                str(Path(__file__).parent / 'vector.svg')
            )
#/codeblock


#codeblock Table
def demo_Table():
    with ui.Dialog("Table"):
        with ui.Col():
            ui.Table(
                headers=('Length', '^Width', '>Height'),
                rows=[
                    [21, 34, 56],
                    [65, 87, 98],
                    [21, 32, 54],
                    [65, 76, 87],
                ]
            )
#/codeblock

#codeblock Canvas
def demo_Canvas():

    def render(widget: QWidget, qp: QPainter, ch: ui.CanvasHelper):
        for i in range(10):
            with ch.pen(color=Qt.red, width=1):
                qp.drawRect(QRect(i*10, i*10, 50, 50))
            with ch.pen(color=Qt.darkBlue, width=2):
                qp.drawText(i*10+60, i*10, str(i+1))

    with ui.Dialog("Canvas"):
        ui.Canvas(render, width=300, height=200)

#/codeblock

if __name__ == '__main__':
    if not App.activeDocument():
        App.newDocument('fcapi gui demos')
    with ui.Dialog('Demo', modal=False, size=(400, 600)):
        with ui.Scroll(widgetResizable=True):
            with ui.Container():
                demos = ((n, fn) for n, fn in dict(globals()).items() if n.startswith('demo_'))
                for n, fn in sorted(demos, key=lambda x: x[0]):
                    ui.button(label=n[5:])(fn)
