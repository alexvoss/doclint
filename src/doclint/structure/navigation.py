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
Abstract base class for representation of a hierarchical navigation structure.
Supports navigation up and down the hierarchy but not between siblings.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence
from doclint.structure.content import Content

@dataclass(kw_only=True)
class NavLevel(ABC):
    """
    A base class for representing elements of the navigation structure.
    Inherit from this to create a more specific navigation structure to
    match specific types of content, while allowing heuristics to work
    with this more generic base class.

    Each navigation node can have content attached. In some systems, content
    only ever appears in leaf nodes, in which case the content lists higher
    up in the tree will simply be empty.
    """
    name: str | None         # human-readable name
    parent: NavLevel | None  # None if root of the hierarchy

    @abstractmethod
    def is_root(self) -> bool:
        """
        Returns True if the node is the root of the navigation hierarchy,
        False otherwise.
        """

    @abstractmethod
    def has_children(self) -> bool:
        """
        Returns True if the navigation node has child nodes, False otherwise.
        """

    @abstractmethod
    def children(self) -> list[NavLevel]:
        """
        A method for getting all the children of the navigation node, empty
        list if there are none.
        """

    @abstractmethod
    def has_content(self) -> bool:
        """
        Returns true if there is content attached to this node, False otherwise.
        """

    @abstractmethod
    def content(self) -> Sequence[Content]:
        """
        Returns a list of Content objects, empty list if there are none.
        """

    def get_depth(self) -> int:
        """
        Return the depth of navigation that this node sits at.
        """
        return 1 + self.parent.get_depth() if self.parent is not None else 0

    def get_path(self):
        """
        Print the path to this navigation node.
        """
        parent_path = self.parent.get_path() if self.parent is not None else ""
        return parent_path + "/" + str(self.name)