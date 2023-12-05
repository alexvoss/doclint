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
Report on the navigation structure.
"""
from rich.console import Console

from ..structure.navigation import NavLevel
from ..heuristics.heuristic import Heuristic, HeuristicTypeException
from ..heuristics.heuristic import get_heuristics
from ..heuristics import navigation

console = Console(highlight= False, record=True)
heuristics = get_heuristics('doclint.heuristics.navigation')

def print_help():
    print("[bold magenta]World[/bold magenta]")
    pass

def report(node: NavLevel, output = None):
    """
    Report that lists the navigation structure and applies checks such as for
    a maximum allowed depth or the maximum allowed number of elements at each
    level.
    """
    check_navlevel(node)
    if node.has_children():
        for child in node.children():
            if child is not None:
                report(child)
    
    if output is not None:
        html = console.export_html()
        with open(output, 'w', encoding = 'utf8') as fd:
            fd.write(html)

def check_navlevel(node) -> None:
    """
    Run heuristics on the given navigation level and write results to the
    console.
    """
    console.print(f"[magenta]{node.get_path()}[/magenta]")
    for heuristic in heuristics:
        passes_this = heuristic.passes(node)
        if not passes_this:
            console.print(f"❌ {heuristic.identifier()}")
            console.print(f"[red]{heuristic.description()}[/red]")
    
