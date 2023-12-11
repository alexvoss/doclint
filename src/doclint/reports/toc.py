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
Report that prints the navigation structure in the form of a table of contents.
"""

from rich.console import Console
from doclint.structure.content import \
    DiscussionContent, HTMLContent, ProblemContent, UnknownContent, VideoContent

from ..structure.navigation import NavLevel

console = Console(highlight= False, record=True)


def print_help():
    print("[bold magenta]World[/bold magenta]")
    pass

def report(node: NavLevel, output = None):
    """
    Report that prints a table of content.
    """
    report_level(node)
    # TODO: produce HTML output!

def report_level(
        node: NavLevel, 
        *,
        indent: int = 0,
        numbering: str = ""
    ):
    """
    Print the ToC line for a specfic navigation level and its children.
    """
    _number = 1
    for child in node.children():
        if child is None: continue        
        
        _numbering = f"{numbering}.{_number}" if numbering != "" else f"{_number}"
        _content = get_content_logo(child) 
        _indenting = "  " * indent 
        if child.name is not None:    
            if child.include_in_toc():        
                console.print(f"{_indenting}{_numbering} {child.name}{_content}")
            _number += 1
            report_level( 
                node = child, 
                indent = indent + 1,
                numbering = _numbering
            )
   
def get_content_logo(node: NavLevel):
    """
    Return a sequence of logos for content in the given navigation node.
    """
    if not node.has_content():        
        return ""
    _icons = []
    for content in node.content():
        match(content):
            case HTMLContent():
                _icons.append("🗎")
                if contains_images(content):
                    _icons.append("🖽")
            case VideoContent():
                _icons.append("🎥")
            case ProblemContent():
                _icons.append("✔")
            case DiscussionContent():
                _icons.append("🗪")
            case UnknownContent():
                _icons.append("≟")
            case _:
                _icons.append("OOPS, error, genuinely unknown content encountered.")
    if len(_icons) == 0:
        return ""
    iconslist = ','.join(_icons)
    return f" {iconslist}"

def contains_images(html: HTMLContent) -> bool:
    return html.content.find("img") is not None