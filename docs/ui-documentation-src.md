:comment
    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

    (c) 2024 Frank David Martínez Muñoz.
:/comment

~:doc:PRE:~

# FreeCAD GUI Modern API


~:doc:META:~


~:doc:TOC:~


~:doc:page-break:~

# Preliminaries

## Disclaimer

All of the following information is the result of my own research and usage of
the FreeCAD's Python APIs and Qt/PySide along several years. It reflects my very
own view, coding style and limited understanding of FreeCAD internals. All the
content is based on official docs, forum discussions, development of my own
extensions, reading code of existing extensions and FreeCAD sources.

This document does not cover 100% of the Qt/PySide API because it is huge and not
really required for common Macros in FreeCAD.


## Audience

This is a technical document for developers of FreeCAD extensions using Qt/PySide
as they GUI Framework.

General programming experience, some basic FreeCAD know-how and a minimalistic
comprehension of Python are sufficient, as long as you can search the internet
for a basic grasp of classes, functions, decorators, type hints, etc...;)

It is also expected that the readers are FreeCAD users, and have a good
understanding of the basic usage of it.


## Goals

* The API must be developer friendly, consistent, maintainable and compatible
  with FC 0.21+
* The API must be an overlay on top of the existing PySide API, so no conflicts
  with existing code.
* The API must be 100% documented.


## Non Goals

* It is not intended to replace anything in the existing FreeCAD APIs.
* It is not intended to require any refactoring of existing python code.
* It is not intended to require any refactoring of existing C/C++ code.


~:doc:page-break:~

# Features

- [x] Declarative Layout
  - [x] Code layout reflects GUI Structure
- [x] Custom input widgets
  - [X] InputText
  - [X] Numeric inputs: InputInt, InputFloat, InputQuantity
  - [X] List inputs: InputFloatList
  - [X] InputBoolean
  - [X] InputVector
  - [X] InputOptions
  - [X] Selection input: InputSelectOne, InputSelectMany
  - [X] Buttons
- [x] Custom view widgets
  - [x] Html
  - [x] Image
  - [x] Svg
  - [x] Table
  - [x] Canvas
- [x] Documentation in markdown format.


~:doc:page-break:~

# Widgets

## Containers / Layouts

~:widget:Dialog:~
~:widget:Scroll:~
~:widget:GroupBox:~
~:widget:Container:~
~:widget:TabContainer:~
~:func:Tab:~
~:widget:Splitter:~
~:widget:Col:~
~:widget:Row:~

## Output

~:widget:TextLabel:~
~:widget:Html:~
~:widget:ImageView:~
~:widget:SvgImageView:~
~:widget:Table:~
~:widget:Canvas:~

## Inputs

~:widget:InputBoolean:~
~:widget:InputInt:~
~:widget:InputFloat:~
~:widget:InputFloatList:~
~:widget:InputQuantity:~
~:widget:InputVector:~
~:widget:InputText:~
~:widget:InputOptions:~
~:widget:InputSelectOne:~
~:widget:InputSelectMany:~
~:widget:button:~

## Layout tools

~:func:Stretch:~
~:func:Spacing:~

; ------------------------------------------------------------------------------


:build-options

[toc]
depth = 3

[widget]
header-level = 3

:/build-options