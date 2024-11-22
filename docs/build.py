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

# !!! THIS IS NOT PUBLIC API !!!

"""
Compiles documentation-src.md into documentation.md

Additional formats documentation.html and documentation.pdf are manually generated
from documentation.md using typora.
"""

import re
import datetime
import ast
from textwrap import indent, dedent
from typing import Dict, Any
from pathlib import Path
from configparser import ConfigParser

# Embedded code blocks
# ```
# code...
# ```
CODE_BLOCK = re.compile(
    r"```(?P<content>.*?)```",
    re.DOTALL,
)

# Pattern to find code blocks in external files
# #codeblock name
# code ...
# #/codeblock
EXTERNAL_CODE_BLOCK = re.compile(
    r"^#\s*codeblock([ \t](\w+))?[\r\n]+(.*?)#/\s*codeblock",
    re.MULTILINE | re.DOTALL,
)

# Patter to include external code
# file_name[block_name][indent]
INCLUDE_CODE = re.compile(r"(.*?)(\[(.*?)\])?(\[(.*?)\])?")

# Markdown headers
# # Header 1 ...
# ## Header 2 ...
# ### Header 3 ...
HEADERS = re.compile(r"(?m)^(#+)\s+(.*)$")

# Macros:
# ~:doc:META:~          Generate table of meta tags
# ~:doc:TOC:~           Generate table of content
# ~:doc:date:~          Current date
# ~:doc:page-break:~    Insert manual page break
# ~:func:name:~         Include function reference documentation from fpo
# ~:class:name:~        Include class reference documentation from fpo
# ~:a:name:~            Generate a named anchor
# ~:code:path:~         Include source code as code block
# ~:widget:name:~       Include widget function section
MACRO = re.compile(r"~:(doc|func|class|a|code|widget):(.+?):~")

# docstring parsing
# - :param type name: description
# - :return type: description
DOC_PARAM = re.compile(r":param\s+(.+?)\s+(\**\w+)\s*:\s*(.+)")
DOC_RETURN = re.compile(r":return\s+(.+?)\s*:\s*(.+)")

# Comments in the documentation source
INTERNAL_LINE_COMMENTS = re.compile(r"^; .*?$", re.MULTILINE)
INTERNAL_BLOCK_COMMENTS = re.compile(r":comment\s+(.*?):/comment(\s)", re.DOTALL)

# Build options
BUILD_OPTIONS = re.compile(r":build-options\s+(.*?):/build-options", re.DOTALL)


# Build options to control the generator
# ──────────────────────────────────────────────────────────────────────────────
class BuildOption:
    def __init__(self, name: str, kind: type, default: Any):
        self.name = name
        self.kind = kind
        self.value = default

    def set(self, value: any):
        self.value = self.kind(value)

    def __repr__(self):
        return f"{self.name}={self.value}"


opt_toc_depth = BuildOption("toc-depth", int, 3)
opt_widget_h_level = BuildOption("widget-header-level", int, 1)
opt_fn_h_level = BuildOption("function-header-level", int, 3)

OPTIONS = {v.name: v for v in globals().values() if isinstance(v, BuildOption)}


# Parsed function info
# ──────────────────────────────────────────────────────────────────────────────
class Function:
    def __init__(self, name: str, node: ast.FunctionDef, cls_doc: str = None):
        self.name = name
        self.doc = ast.get_docstring(node) or cls_doc or ""
        self.sig = ast.unparse(node.args)
        ret = " -> " + ast.unparse(node.returns) if node.returns else ""
        # Hide self argument
        args = re.sub(r"^(self|cls)(\s*,\s*)?", "", self.sig)
        # Format one argument per line
        if len(args) + len(ret) > 70:
            args = re.sub(r"(\w+\s*[:]|\*+)", r"\n        \1", args) + "\n    "
        self.decl = f"def {self.name}({args}){ret}: ..."


# Generate Table of content (TOC)
# ──────────────────────────────────────────────────────────────────────────────
def generate_toc(content: str) -> str:
    max_depth = opt_toc_depth.value
    toc = ["\n\n# TABLE OF CONTENTS\n"]
    content_without_code_blocks = CODE_BLOCK.sub("", content)
    for header in HEADERS.findall(content_without_code_blocks):
        level = header[0].count("#")
        if level > max_depth:
            continue
        h = header[1].strip()
        if "`" not in h:
            indent = "    " * (level - 1)
            link = re.sub(r"\W+", "-", h.lower()).strip("-")
            toc.append(f"{indent}{'*' if indent else '*'} [{h}](#{link})\n")
    return "".join(toc)


# Markdown table generator
# ──────────────────────────────────────────────────────────────────────────────
def md_table(*cols):
    header = " " + "| ".join((c[0].ljust(c[1]) for c in cols))
    sep = "|".join(("-" * (c[1] + 1) for c in cols))
    data = []

    def table() -> str:
        if len(data) == 0:
            return ""
        rows = (header, sep, *data)
        return "\n" + "\n".join((f"|{row}|" for row in rows))

    def add(*row):
        data.append(" " + "| ".join((row[c].ljust(cols[c][1]) for c in range(len(cols)))))

    table.add = add
    return table


# Get meta
# ──────────────────────────────────────────────────────────────────────────────
def get_meta(source: ast.Module) -> Dict[str, Any]:
    tags = dict()

    class NT(ast.NodeTransformer):
        def visit_Assign(self, node):
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                if (
                    var_name.startswith("__")
                    and var_name.endswith("__")
                    and node.targets[0].col_offset == 0
                ):
                    tags[var_name] = str(node.value.value)
            return node

    NT().visit(source)
    return tags


# Generate a table of meta-tags
# ──────────────────────────────────────────────────────────────────────────────
def generate_meta(source: ast.Module):
    meta = get_meta(source)
    table = md_table(("META", 18), ("VALUE", 50))
    table.add("__generated__", str(datetime.datetime.now()))
    for row in meta.items():
        table.add(*row)
    return table()


# Generate yaml preamble
# ──────────────────────────────────────────────────────────────────────────────
def generate_preamble(source: ast.Module):
    meta = get_meta(source)
    content = ["---"]
    for name, value in meta.items():
        content.append(f'{name.replace("__", "")}: "{str(value)}"'.replace("\n", ""))
    content.append(f'date: "{datetime.datetime.now()}"')
    content.append('geometry: "margin=2cm"')
    content.append("---")
    return "\n".join(content)


# Interpolate all Macros
# ──────────────────────────────────────────────────────────────────────────────
def interpolate_macros(content: str, source: ast.Module, base_dir: Path) -> str:
    functions = []

    def interpolate(m: re.Match):
        kind, ident = m.groups()
        if kind == "doc":
            if ident == "TOC":
                return "___TOC___"
            if ident == "META":
                return generate_meta(source)
            if ident == "PRE":
                return generate_preamble(source)
            if ident == "date":
                return f"{datetime.datetime.now()}"
            if ident == "page-break":
                return '<p style="page-break-after: always; break-after: page;"></p>\n'
        elif kind == "a":
            return f"<a name='{ident}'></a>"
        elif kind == "func":
            if not functions:
                functions.append(parse_functions(source))
            return function_md(ident, functions[0], base_dir, opt_fn_h_level.value)
        elif kind == "widget":
            if not functions:
                functions.append(parse_functions(source))
            return widget_md(ident, functions[0], base_dir)
        elif kind == "code":
            return include_file_as_code(ident, base_dir)

    return MACRO.sub(interpolate, content)


_included_code_cache = dict()


def include_file_as_code(ident: str, base_dir: Path) -> str:
    file_name, _, block_name, __, indent_n = INCLUDE_CODE.fullmatch(ident).groups()
    if not indent_n:
        indent_n = 0
    else:
        indent_n = int(indent_n)
    cached = _included_code_cache.get((file_name, block_name), None)
    if cached:
        return cached
    src = base_dir / file_name
    if src.exists():
        with open(src, "r") as f:
            for _, code_block_name, code in EXTERNAL_CODE_BLOCK.findall(f.read()):
                text = f"> *{file_name}* ({code_block_name})\n\n"
                text += f"""\n```python\n{code}\n```\n"""
                _included_code_cache[(file_name, code_block_name)] = indent(dedent(text), ' ' * indent_n)
        cached = _included_code_cache.get((file_name, block_name), None)
        if not cached:
            return f"ERROR: BLOCK NOT FOUND: {block_name}"
        return cached
    return f"ERROR: FILE NOT FOUND: {file_name}"


# Remove comments, documentation is code, so there are comments that are not
# expected to see in the generated doc.
# ──────────────────────────────────────────────────────────────────────────────
def remove_comments(content):
    s = INTERNAL_BLOCK_COMMENTS.sub("", content)
    s = INTERNAL_LINE_COMMENTS.sub("", s)
    return s


# Markdown does not support line-breaks inside tables, this allows to use
# char + to mark a continuation.
# ──────────────────────────────────────────────────────────────────────────────
def fix_tables(content):
    TABLE = re.compile(r"^:table(.*?):/table$", re.MULTILINE | re.DOTALL)

    def fix(m):
        return re.sub(r"(?<!\\)\+\s+", "", m.group(1), 0, re.MULTILINE)

    return TABLE.sub(fix, content)


# Generate a table of arguments from a docstring
# ──────────────────────────────────────────────────────────────────────────────
def params_table(comment: str):
    if not comment:
        return ""

    table = md_table(("Argument", 15), ("Type", 15), ("Description", 43))
    for m in DOC_PARAM.finditer(comment):
        type_, name, doc = m.groups()
        type_ = type_.replace("|", r"\|")
        table.add(name, type_, doc)
    return table()


# Generate a return block from a docstring
# ──────────────────────────────────────────────────────────────────────────────
def return_table(comment: str):
    if not comment:
        return ""
    table = md_table(("Return type", 15), ("Description", 50))
    for m in DOC_RETURN.finditer(comment):
        type_, doc = m.groups()
        table.add(type_, doc)
    return table()


# Generate markdown from a docstring
# ──────────────────────────────────────────────────────────────────────────────
def comment_md(doc, base_dir: Path):
    doc = dedent(doc)
    args = params_table(doc)
    doc = DOC_PARAM.sub("", doc)
    ret = return_table(doc)
    doc = DOC_RETURN.sub("", doc)
    doc = interpolate_macros(doc, None, base_dir)
    return "\n".join((ret, args, "\n", doc.strip())).rstrip()


# Generate a function reference documentation
# ──────────────────────────────────────────────────────────────────────────────
def widget_md(name: str, functions: Dict[str, Function], base_dir: Path):
    block = f"""{function_md(name, functions, base_dir, opt_widget_h_level.value, "Widget")}
    """
    return block


def fn_image(name: str) -> str:
    return (
        f'<p style="align: center; border: 1px solid black"><img src="images/fn_{name}.png" /></p>'
    )


# Generate a function reference documentation
# ──────────────────────────────────────────────────────────────────────────────
def function_md(
    name: str, functions: Dict[str, Function], base_dir: Path, header_level=3, prefix="Function"
):
    func = functions[name]
    name = re.sub(r"__(.*)", "\\__$1", name)

    content = [
        f"{'#' * header_level} {prefix}: {func.name}",
        f"{'#' * (header_level + 1)} Signature / {func.name}",
        f"```python\n{func.decl}\n```\n",
    ]

    img = base_dir / "images" / f"fn_{name}.png"
    if img.exists():
        content.append(f"{'#' * (header_level + 1)} Gui / {func.name}")
        content.append(fn_image(name))

    if func.doc:
        content.append(f"{'#' * (header_level + 1)} Docs / {func.name}")
        content.append(comment_md(func.doc, base_dir))

    return "\n\n".join(content)


# Generate a function reference documentation
# Reduce more than 3 consecutive blank lines to 3
# ──────────────────────────────────────────────────────────────────────────────
def clean_blank_lines(content: str) -> str:
    return re.sub("\n\n\n\n+", "\n\n\n", content)


# Extract function information
# ──────────────────────────────────────────────────────────────────────────────
def parse_functions(source: ast.Module) -> Dict[str, Function]:
    functions = dict()

    class NT(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            functions[node.name] = Function(node.name, node)
            return node

        def visit_ClassDef(self, node: ast.ClassDef):
            doc = ast.get_docstring(node)
            init = [n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"]
            if init:
                functions[node.name] = Function(node.name, init[0], doc)
            return node

    NT().visit(source)
    return functions


def parse_build_options(content: str):
    opts = BUILD_OPTIONS.findall(content)
    if len(opts) > 1:
        raise RuntimeError("Only one build-options section is allowed")
    if len(opts) == 1:
        config = ConfigParser()
        config.read_string(opts[0])
        for section in config.sections():
            for key, val in config.items(section):
                OPTIONS[f"{section}-{key}"].set(val)
    return BUILD_OPTIONS.sub("", content)


# Compile *-src.md
# ──────────────────────────────────────────────────────────────────────────────
def build(source_doc: str, module_name: str):
    _included_code_cache.clear()
    base = Path(Path(__file__).parent)
    doc_src_file = Path(base, f"{source_doc}-src.md")
    with open(doc_src_file, "r") as file:
        content = file.read()
        content = parse_build_options(content)
        with open(base.parent / f"{module_name}.py", "r") as mod_src:
            source = ast.parse(mod_src.read(), type_comments=True)
        content = remove_comments(content)
        content = fix_tables(content)
        content = interpolate_macros(content, source, base)
        content = clean_blank_lines(content)
        content = content.replace("___TOC___", generate_toc(content), 1)
        with open(Path(base, f"{source_doc}.md"), "w") as out:
            out.write(content.strip())


# Main
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build("documentation", "fpo")
    build("ui-documentation", "fcui")
