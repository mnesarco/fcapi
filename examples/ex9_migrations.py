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

from fpo import (
    proxy, PropertyInteger, PropertyLength, PropertyAngle, PropertyLink,
    print_log, migrations, print_err)


# Lets create a minimal ScriptedObject with a bunch of properties and some migrations
#
# 1. Create a document in FreeCAD, add an instance of the Object
# 2. Save the document
# 3. Close FreeCAD
# 4. Change the version of the class here in the decorator
# 5. Open FreeCAD
# 6. Open your saved file, as the versions differ, you will see the messages in
#    the console of your migrations
# 7. Save and close your file (it will be saved with the new version)
# 8. Reopen your file, migrations won't run because versions match.

@migrations()
@proxy(version=1)
class MyDataVersioned:

    elements = PropertyInteger(default=3)
    thickness = PropertyLength(default=1)
    angle = PropertyAngle(default=30)
    source = PropertyLink()

    def on_migrate_upgrade(self, version: int, fp):
        print_log(f"your code runs here")
        self.set_version(2)
        
    def on_migrate_downgrade(self, version: int, fp):
        print_log(f"your code runs here")
        self.set_version(1)
        
    def on_migrate_complete(self, version: int, fp):
        print_log(f"your code runs here")
        
    def on_migrate_error(self, version: int, fp):
        print_err(f"your code runs here")


# Use by just calling the create method from a macro or directly from the python
# console
def create_data():
    return MyDataVersioned.create(name="V1")

