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

from __future__ import annotations

import fpo
import fcapi_test.framework as utx

class TestProperty(utx.FCApiTestCase):
    def setUp(self):
        self.init_doc()
        self.obj = self.doc.addObject("App::FeaturePython")
        self.prop = fpo.Property(
            type="App::PropertyInteger",
            name="Length",
            section='Data',
            default=42,
        )

    def test_create(self):
        obj = self.obj
        prop = self.prop

        prop.create(obj)

        self.assertTrue("Length" in obj.PropertiesList)
        self.assertTrue(obj.getTypeIdOfProperty("Length"), "App::PropertyInteger")
        self.assertTrue(obj.getGroupOfProperty('Length'), 'Data')
        self.assertTrue(obj.Length, 42)


    def test_reset(self):
        obj = self.obj
        prop = self.prop

        prop.create(obj)
        obj.Length = 100
        self.assertTrue(obj.Length, 100)
        prop.reset(obj)
        self.assertTrue(obj.Length, 42)
