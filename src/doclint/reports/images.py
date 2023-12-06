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
Report on embedded images.
"""
from rich.console import Console

from ..structure.navigation import NavLevel
from ..structure.content import HTMLContent
from ..heuristics.heuristic import Heuristic, HeuristicTypeException
from ..heuristics.heuristic import get_heuristics
from ..heuristics import images

console = Console(highlight= False, record=True)
heuristics = get_heuristics('doclint.heuristics.images')

def print_help():
    print("[bold magenta]World[/bold magenta]")
    pass

def report(node: NavLevel, output = None):
    """
    Checks all images
    """
    if node.has_content():
        for content in node.content():
            if isinstance(content, HTMLContent):
                check_images(content, node)
    if node.has_children():
        for child in node.children():
            if child is not None:
                report(child)

    if output:
        html = console.export_html()
        with open(output, 'w', encoding = 'utf8') as fd:
            fd.write(html)

def check_images(content: HTMLContent, parent: NavLevel):
    console.print(f"[magenta]{parent.get_path()}[/magenta]")
    for image in content.images():
        for heuristic in heuristics:
            if not heuristic.passes(image):
                console.print(f"❌ {image.src}")
                console.print(f"[red]{heuristic.description()}[/red]")