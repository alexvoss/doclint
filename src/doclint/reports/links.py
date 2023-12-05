# =============================================================================
# MIT License
#
# Copyright (c) 2023 Alexander Voss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================

"""
Report that checks links - link text, URL and attributes.
"""

import inspect
import sys
from typing import Sequence, Tuple

from rich.console import Console
from ..structure.navigation import NavLevel
from ..structure.content import Link
from ..heuristics import links
from ..heuristics.heuristic import Heuristic, HeuristicTypeException
from ..heuristics.heuristic import get_heuristics

console = Console(highlight=False, record=True)
heuristics = get_heuristics('doclint.heuristics.links')

def print_help():
    print("[bold magenta]World[/bold magenta]")
    pass


def report(node: NavLevel, output = None):
    """
    Lists all the links in the content and adds the results of applying
    link heuristics.
    """
    if node.has_content():
        for content in node.content():
            check_links(content.links(), node)
    if node.has_children():
        for child in node.children():
            if child is not None:
                report(child)
    if output:
        html = console.export_html()
        with open(output, 'w', encoding='utf8') as fd:
            fd.write(html)


def check_links(links: list[Link], parent: NavLevel):
    """
    Iterate over links, run heuristics, report results
    """
    if len(links) == 0:
        return
    console.print(f"[magenta]{get_path(parent)}[/magenta]")
    for link in links:
        (success, failures) = check_link(link)
        if success:
            console.print(f"✅ {link.text} -> {link.url}")
        else:
            console.print(f"❌ {link.text} -> {link.url}")
            for failure in failures:
                console.print(f"   [red]{failure.identifier()}: {failure.description()}[/red]")


def check_link(link: Link) -> Tuple[bool, Sequence[type[Heuristic]]]:
    """
    Returns a tuple with the first element indicating if all heuristics
    passed (True) or at least one failed (False). The second element is a
    list of identifiers of those heuristics that failed to pass.
    """
    
    passes: bool = True
    failures: list[type[Heuristic]] = []
    for heuristic in heuristics:
        passes_this = heuristic.passes(link)
        if not passes_this:
            passes = False
            failures.append(heuristic)
    return (passes, failures)


def get_path(node: NavLevel):
    """
    Print the path to the navigation node given.
    """
    path = get_path(node.parent) if node.parent is not None else "/"
    return path + "/" + str(node.name)
