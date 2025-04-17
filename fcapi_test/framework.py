# Copyright 2024 Frank David Martinez M (mnesarco)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ruff: noqa

"""Small framework for fcapi tests.

FreeCAD does not ship with pytest, so here are some
utilities to use with unittest instead.
"""

import unittest as ut
import FreeCAD as App

class FCApiTestCase(ut.TestCase):

    doc_name: str
    doc: App.Document

    def shortDescription(self):
        return None

    def init_doc(self, name: str = None):
        self.doc_name = name or self.__class__.__name__
        try:
            self.doc = App.getDocument(self.doc_name)
        except Exception:
            self.doc = App.newDocument(self.doc_name)
            self.doc_name = self.doc.Name
        App.setActiveDocument(self.doc_name)

    def tearDown(self):
        if hasattr(self, 'doc') and self.doc:
            App.closeDocument(self.doc.Name)