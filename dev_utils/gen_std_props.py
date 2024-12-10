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

"""Generator of Property constructors."""

# ruff: noqa: PTH123, T201

import re
import sys
from pathlib import Path

DIR = Path(__file__).parent
PROP = re.compile(r"App::(Property\w+)\s*::init\(\);")

EXCLUDE = {
    "PropertyContainer",
    "PropertyExpressionContainer",
    "PropertyXLinkContainer",
    "PropertyLinkBase",
    "PropertyLinkListBase",
    "PropertyLists",
    "PropertyEnumeration",
}

def main(src: Path) -> None:
    """Extract Property classes initialized in Application.cpp from FreeCAD sources."""
    with open(Path(DIR, "generated_properties.py"), "w") as fout:
        for path in src.glob("**/Application.cpp"):
            fout.write(f"##: Generated from <FreeCAD_sources>/src/App/{path.name}\n")
            fout.write("##: Supported Property types\n")
            fout.write(f"##: {'─' * 77}\n")

            print(f"Extracting from: {path}")
            with open(path) as file:
                cpp = file.read()
                all_unique = sorted(set(PROP.findall(cpp)))
                for p in all_unique:
                    print(f"Found property: {p}")
                    if p not in EXCLUDE:
                        fout.write(f'{p} = _prop_constructor("App::{p}")\n')

if __name__ == "__main__":
    main(Path(sys.argv[1]))
