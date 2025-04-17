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

"""Unit tests for fpo."""

from __future__ import annotations

import unittest as ut
import fpo
import fcapi_test.framework as utx
from pathlib import Path
import inspect


class TestArity(utx.FCApiTestCase):
    def test_f_arity(self):
        """Arity of a function is the number of its formal arguments."""

        def noargs(): ...
        def one_arg(arg): ...
        def two_args(a, b): ...
        def many_but_three(a, *args, **kwargs): ...

        self.assertEqual(fpo._f_arity(noargs), 0)
        self.assertEqual(fpo._f_arity(one_arg), 1)
        self.assertEqual(fpo._f_arity(two_args), 2)
        self.assertEqual(fpo._f_arity(many_but_three), 3)

    @ut.expectedFailure
    def test_m_arity_no_method(self):
        """Instance methods must have at least one argument (self)"""

        def noargs(): ...

        fpo._m_arity(noargs)

    def test_m_arity(self):
        """Arity of a method is the number of arguments excluding self"""

        def one_arg(self): ...
        def two_args(self, b): ...
        def many_but_three(self, *args, **kwargs): ...

        self.assertEqual(fpo._m_arity(one_arg), 0)
        self.assertEqual(fpo._m_arity(two_args), 1)
        self.assertEqual(fpo._m_arity(many_but_three), 2)


class TestCall(utx.FCApiTestCase):
    def test_call_non_existent(self):
        """_call can call non existent functions"""

        class Obj:
            pass

        self.assertEqual(fpo._call(Obj(), "some_method", 1, 2, 3, a=1), None)

    def test_call_existent(self):
        """_call calls a function if exists"""

        class Obj:
            def some_method(self, arg):
                return 2 * arg

        self.assertEqual(fpo._call(Obj(), "some_method", 1), 2)


class TestNaming(utx.FCApiTestCase):
    def test_snake_to_camel(self):
        self.assertIsNone(fpo._snake_to_camel(None))
        self.assertEqual(fpo._snake_to_camel("_a"), "A")
        self.assertEqual(fpo._snake_to_camel("a"), "A")
        self.assertEqual(fpo._snake_to_camel("a_"), "A")
        self.assertEqual(fpo._snake_to_camel("a_b"), "AB")
        self.assertEqual(fpo._snake_to_camel("call"), "Call")
        self.assertEqual(fpo._snake_to_camel("_call"), "Call")
        self.assertEqual(fpo._snake_to_camel("__call"), "Call")
        self.assertEqual(fpo._snake_to_camel("hello_world"), "HelloWorld")
        self.assertEqual(fpo._snake_to_camel("hello_World"), "HelloWorld")
        self.assertEqual(fpo._snake_to_camel("Hello_World"), "HelloWorld")
        self.assertEqual(fpo._snake_to_camel("Hello_world"), "HelloWorld")
        self.assertEqual(fpo._snake_to_camel("Hello_world_"), "HelloWorld")
        self.assertEqual(fpo._snake_to_camel("hello__world_"), "HelloWorld")
        self.assertEqual(fpo._snake_to_camel("HelloWorld"), "Helloworld")


class TestUriResolver(utx.FCApiTestCase):
    def test_resolve_uri(self):
        base = Path("/some/base/path")
        self.assertEqual(fpo._resolve_uri("/absolute", base), "/absolute")
        self.assertEqual(fpo._resolve_uri("/absolute", None), "/absolute")
        self.assertEqual(fpo._resolve_uri("self:child", None), "self:child")
        self.assertEqual(Path(fpo._resolve_uri("self:child", base)), Path("/some/base/path/child"))


class TestPropertyConstructors(utx.FCApiTestCase):
    def test_prop_constructor(self):
        c = fpo._prop_constructor("App::PropertyInteger")
        self.assertTrue(callable(c))
        self.assertEqual(inspect.signature(c).return_annotation, "Property")


class TestTypePredicates(utx.FCApiTestCase):
    def test_single(self):
        predicate = fpo._is(int)
        self.assertTrue(predicate(5))
        self.assertFalse(predicate(5.1))
        self.assertFalse(predicate(None))
        # Special case, bool is also int
        self.assertTrue(predicate(True))
        self.assertFalse(predicate("5"))

    def test_many(self):
        predicate = fpo._is((float, str))
        self.assertFalse(predicate(5))
        self.assertTrue(predicate(5.1))
        self.assertFalse(predicate(None))
        self.assertFalse(predicate(True))
        self.assertFalse(predicate(False))
        self.assertTrue(predicate("5"))


class TestMembers(utx.FCApiTestCase):
    def test_get_properties(self):
        class X:
            ident = fpo.PropertyInteger()
            name = fpo.PropertyString()

        props = fpo._get_properties(X)
        self.assertEqual(len(props), 2)
        self.assertEqual(props[0][0], "ident")
        self.assertEqual(props[1][0], "name")
        self.assertIsInstance(props[0][1], fpo.Property)
        self.assertIsInstance(props[1][1], fpo.Property)

    def test_get_properties_0(self):
        class X:
            pass

        props = fpo._get_properties(X)
        self.assertEqual(len(props), 0)

    def test_get_display_modes(self):
        class X:
            wireframe = fpo.DisplayMode()
            default = fpo.DisplayMode()

        modes = fpo._get_display_modes(X)
        self.assertEqual(len(modes), 2)
        self.assertEqual(modes[0][0], "default")
        self.assertEqual(modes[1][0], "wireframe")
        self.assertIsInstance(modes[0][1], fpo.DisplayMode)
        self.assertIsInstance(modes[1][1], fpo.DisplayMode)

    def test_get_display_modes_0(self):
        class X:
            pass

        modes = fpo._get_display_modes(X)
        self.assertEqual(len(modes), 0)


class TestForwardMethod(utx.FCApiTestCase):
    @ut.expectedFailure
    def test_should_not_override(self):
        class X:
            def method_from(self):
                pass

            def method_to(self):
                pass

        fpo._t_forward(X, "method_from", "method_to")

    def test_forward(self):
        class X:
            def method_to(self):
                return True

        fpo._t_forward(X, "method_from", "method_to")
        instance = X()
        self.assertEqual(instance.method_from(), True)

    def test_no_target_no_forward(self):
        class X:
            pass

        fpo._t_forward(X, "method_from", "method_to")
        instance = X()
        self.assertFalse(hasattr(instance, "method_from"))


