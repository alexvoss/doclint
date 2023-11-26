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

from urllib.parse import urlparse
from ..structure.content import Link
from .heuristic import Heuristic, HeuristicTypeException

class CheckLinkText(Heuristic):
    """links should have descriptive link texts, not `here` or `this page`."""
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
            or re.fullmatch(r"^here$", link.text) \
            or link.text == "this link" \
            or link.text == "this page":
            return (False, cls)
        return (True, cls)

class CheckUrl(Heuristic):
    """URLs need to be valid."""
    description = __doc__
    identifier = "dl-link-url-valid"

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
        try:
            urlparse(link.url)
        except ValueError:
            return (False, cls)
        return (True, cls)

class CheckUrlNoSearch(Heuristic):
    """URLs should not point to search results or search engine redirects."""
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
            return (False, cls)
        return (True,  cls)
