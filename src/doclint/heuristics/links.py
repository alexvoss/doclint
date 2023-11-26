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
Heuristics for Links.
"""

import re

from ..structure.content import Link
from .heuristic import Heuristic, HeuristicTypeException

class CheckLinkText(Heuristic):
    """Check for non-descriptive link texts such as `here` or `this page`."""
    description = __doc__
    identifier = "dl-link-text"

    @classmethod
    def applies_to(cls, item) -> bool:
        return isinstance(item, Link)

    @classmethod
    def applies_to_types(cls):
        return [Link]

    @classmethod
    def passes(cls, item) -> (bool, str):
        if not isinstance(item, Link):
            raise HeuristicTypeException(
                f"heuristic {cls.identifier} does not operate on {type(item)}"
            )

        link = item
        if re.fullmatch(r"\Where\W", link.text) \
            or link.text == "this link" \
            or link.text == "this page":
            return (False, cls.identifier)
        return (True, cls.identifier)

# class CheckUrl(Heuristic):
#     """Checks URLs to ensure they are valid."""
#     description = __doc__
#     id = "dl-link-url-valid"

#     def applies_to(item) -> bool:
#         return isinstance(item, Link)

#     def applies_to_types() -> bool:
#         return [Link]

#     def passes(link: Link) -> (bool, str):
#         urllib.parse.

class CheckUrlNoSearch(Heuristic):
    """Checks URLs to ensure they do not point to a search result."""
    description = __doc__
    identifier = "dl-link-url-no-search"

    @classmethod
    def applies_to(cls, item) -> bool:
        return isinstance(item, Link)

    @classmethod
    def applies_to_types(cls) -> bool:
        return [Link]

    @classmethod
    def passes(cls, item: Link) -> (bool, str):
        if not isinstance(item, Link):
            raise HeuristicTypeException(
                f"heuristic {cls.identifier} does not operate on {type(item)}"
            )

        link = item
        if link.url.startswith('https://www.google.com/search') \
            or link.url.startswith('https://www.google.com/url'):
            return (False, cls.identifier)
        return (True,  cls.identifier)
