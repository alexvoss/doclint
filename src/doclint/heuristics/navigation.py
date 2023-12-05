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
Heuristics for navigation structure.
"""

from typing import Sequence
from doclint.structure.navigation import NavLevel
from .heuristic import Heuristic, HeuristicTypeException

class CheckNavSectionLength(Heuristic):
    """
    Navigation sections should have a limited length that does not 
    exceed short-term memory. A number often given is 7 items. 
    This should not, however, be applied at the top level.
    """

    @classmethod
    def identifier(cls) -> str:
        return "dl-nav-length"
    
    @classmethod
    def applies_to(cls, item) -> bool:
        return isinstance(item, NavLevel)
    
    @classmethod
    def applies_to_types(cls) -> Sequence[type]:
        return [NavLevel]
    
    @classmethod
    def passes(cls, item) -> bool:
        if not cls.applies_to(item):
            raise HeuristicTypeException(cls, item)
        nav_level = item
        if len(nav_level.children()) > 7 \
            and nav_level.get_depth() > 1: # ignore the top level
            return False
        return True


class CheckNavSectionDepth(Heuristic):
    """
    Navigation should not be too deeply nested.
    """

    @classmethod
    def identifier(cls) -> str:
        return "dl-nav-depth"
    
    @classmethod
    def applies_to(cls, item) -> bool:
        return isinstance(item, NavLevel)
    
    @classmethod
    def applies_to_types(cls) -> Sequence[type]:
        return [NavLevel]
    
    @classmethod
    def passes(cls, item) -> bool:
        if not cls.applies_to(item):
            raise HeuristicTypeException(cls, item)
        nav_level = item
        if nav_level.get_depth() > 4:
            return False
        return True
    