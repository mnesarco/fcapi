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

"""
Compiles documentation-src.md into documentation.md

Additional formats documentation.html and documentation.pdf are manually generated
from documentation.md using typora.
"""

import re, sys, datetime, ast, inspect
from textwrap import dedent
from typing import Dict, Any, Iterable, Tuple
from pathlib import Path

# Embedded code blocks
CODE_BLOCK  = re.compile(r'```(?P<content>.*?)```', re.DOTALL)

# Markdown headers
HEADERS     = re.compile(r'(?m)^(#+)\s+(.*)$')

# Macros:
# ~:doc:META:~          Generate table of meta tags
# ~:doc:TOC:~           Generate table of content
# ~:doc:date:~          Current date
# ~:doc:page-break:~    Insert manual page break
# ~:func:name:~         Include function reference documentation from fpo
# ~:class:name:~        Include class reference documentation from fpo
# ~:a:name:~            Generate a named anchor
MACRO       = re.compile(r'~:(doc|func|class|a):(.+?):~')

# docstring parsing
# - :param type name: description
# - :return type: description
DOC_PARAM   = re.compile(r':param\s+(.+?)\s+(\**\w+)\s*:\s*(.+)')
DOC_RETURN  = re.compile(r':return\s+(.+?)\s*:\s*(.+)')

# Comments in the documentation source
INTERNAL_LINE_COMMENTS = re.compile(r'^; .*?$', re.MULTILINE)
INTERNAL_BLOCK_COMMENTS = re.compile(r':comment\s+(.*?):/comment(\s)', re.DOTALL)

# Generate Table of content (TOC)
# ──────────────────────────────────────────────────────────────────────────────
def generate_toc(content: str) -> str:
    toc = ["\n\n# TABLE OF CONTENTS\n"]
    content_without_code_blocks = CODE_BLOCK.sub('', content)
    for header in HEADERS.findall(content_without_code_blocks):
        h = header[1].strip()
        if '`' not in h:
            indent = "    " * (header[0].count("#") - 1)
            link = re.sub(r'\W+', '-', h.lower()).strip('-')
            toc.append(f"{indent}{'*' if indent else '*'} [{h}](#{link})\n")
    return "".join(toc)

# Markdown table generator
# ──────────────────────────────────────────────────────────────────────────────
def md_table(*cols):
    header = " " + "| ".join((c[0].ljust(c[1]) for c in cols))
    sep = "|".join(('-' * (c[1]+1) for c in cols))
    data = []
    def table() -> str:
        if len(data) == 0:
            return ''
        rows = (header, sep, *data)
        return "\n" + "\n".join((f"|{row}|" for row in rows))
    def add(*row):
        data.append(" " + "| ".join((row[c].ljust(cols[c][1]) for c in range(len(cols)))))
    table.add = add
    return table


# Get meta
# ──────────────────────────────────────────────────────────────────────────────
def get_meta(source: ast.Module, fpo: Any) -> Dict[str, Any]:
    def is_tag(node):
        return (isinstance(node, ast.Name) 
            and not isinstance(node.ctx, ast.Load) 
                and node.id.startswith('__') 
                    and node.id.endswith('__'))    

    return {node.id: getattr(fpo, node.id) 
            for node in ast.walk(source) if is_tag(node)}


# Generate a table of meta-tags
# ──────────────────────────────────────────────────────────────────────────────
def generate_meta(source: ast.Module, fpo: Any):
    meta = get_meta(source, fpo)
    table = md_table(('META', 18), ('VALUE', 50))
    table.add('__generated__', str(datetime.datetime.now()))
    for row in meta.items():
        table.add(*row)
    return table()


# Generate yaml preamble
# ──────────────────────────────────────────────────────────────────────────────
def generate_preamble(source: ast.Module, fpo: Any):
    meta = get_meta(source, fpo)
    content = ['---']
    for name, value in meta.items():
        content.append(f"{name.replace('__', '')}: {str(value)}".replace('\n', ''))
    content.append(f"date: {datetime.datetime.now()}")
    content.append(f'geometry: "margin=2cm"')
    content.append('---')
    return "\n".join(content)

    
# Interpolate all Macros
# ──────────────────────────────────────────────────────────────────────────────
def interpolate_macros(content: str, source: ast.Module, fpo: Any) -> str:
    def interpolate(m: re.Match):
        kind, ident = m.groups()
        if kind == 'doc':
            if ident == 'TOC':
                return generate_toc(content)
            if ident == 'META':
                return generate_meta(source, fpo)
            if ident == 'PRE':
                return generate_preamble(source, fpo)
            if ident == 'date':
                return f"{datetime.datetime.now()}"
            if ident == 'page-break':
                return '<p style="page-break-after: always; break-after: page;"></p>\n'
        elif kind == 'a':
            return f"<a name='{ident}'></a>"
        elif kind == 'func':
            func =  getattr(fpo, ident)
            return function_md(ident, func)

    return MACRO.sub(interpolate, content)        


# Remove comments, documentation is code, so there are comments that are not
# expected to see in the generated doc.
# ──────────────────────────────────────────────────────────────────────────────
def remove_comments(content):
    s = INTERNAL_BLOCK_COMMENTS.sub('', content)
    s = INTERNAL_LINE_COMMENTS.sub('', s)
    return s


# Markdown does not support line-breaks inside tables, this allows to use
# char + to mark a continuation.
# ──────────────────────────────────────────────────────────────────────────────
def fix_tables(content):
    TABLE = re.compile(r'^:table(.*?):/table$', re.MULTILINE | re.DOTALL)
    def fix(m):
        return re.sub(r'(?<!\\)\+\s+', '', m.group(1), 0, re.MULTILINE)
    return TABLE.sub(fix, content)


# Generate a table of arguments from a docstring
# ──────────────────────────────────────────────────────────────────────────────
def params_table(comment: str):
    if not comment:
        return ''
    
    table = md_table(('Argument', 15), ('Type', 15), ('Description', 43))
    for m in DOC_PARAM.finditer(comment):
        type_, name, doc = m.groups()
        type_ = type_.replace('|', r'\|')
        table.add(name, type_, doc)
    return table()

# Generate a return block from a docstring
# ──────────────────────────────────────────────────────────────────────────────
def return_table(comment: str):
    if not comment:
        return ''
    table = md_table(('Return type', 15), ('Description', 50))
    for m in DOC_RETURN.finditer(comment):
        type_, doc = m.groups()
        table.add(type_, doc)
    return table()

# Generate markdown from a docstring
# ──────────────────────────────────────────────────────────────────────────────
def comment_md(doc):
    doc = dedent(doc)
    args = params_table(doc)
    doc = DOC_PARAM.sub('', doc)
    ret = return_table(doc)
    doc = DOC_RETURN.sub('', doc)
    return "\n".join((doc.strip(), ret, args)).rstrip()

# Generate a function reference documentation
# ──────────────────────────────────────────────────────────────────────────────
def function_md(name: str, func, header_level=3):
    name = re.sub(r'__(.*)', '\\__$1', name)
    sig = str(inspect.signature(func)).replace('fpo.', '')
    block = f"""
    
    {'#' * header_level} *function:* __{name}__

    ```python
    def {name}{sig}
    ```
    """
    return dedent(block) + comment_md(func.__doc__ or '')


# Generate a function reference documentation
# Reduce more than 3 consecutive blank lines to 3
# ──────────────────────────────────────────────────────────────────────────────
def clean_blank_lines(content: str) -> str:
    return re.sub('\n\n\n\n+', '\n\n\n', content)

# Main
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    base = Path(Path(__file__).parent)
    sys.path.append(str(base.parent))    
    doc_src_file = Path(base, 'documentation-src.md')
    import fpo
    with open(doc_src_file, 'r') as file:
        content = file.read()    
        source = ast.parse(inspect.getsource(fpo))
        content = remove_comments(content)
        content = fix_tables(content)
        content = interpolate_macros(content, source, fpo)
        content = clean_blank_lines(content)
        with open(Path(base, 'documentation.md'), 'w') as out:
            out.write(content.strip())

