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
Provides a basis for writing heuristics. The `Heuristic` class provides
basic fields to describe a heuristic as well as a set of methods that are
meant to enable heuristics to be discovered and used dynamically instead
of being hard-coded into reports.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence

BASEURL = "https://corealisation.github.io/doclint/heuristics/"

class Heuristic(ABC):
    """
    Base class for heuristics that gives them an `id`, a (short) `description`
    and a `url` that points to the documentation for that heuristic. There is
    a generic `passes()` method that returns a pass/fail result.
    """

    @classmethod
    @abstractmethod
    def identifier(cls) -> str:
        """
        Return an identifier for this heuristic
        """

    @classmethod
    def description(cls) -> str:
        """
        Return a human-readable description. Default implementation
        returns the class's docstring.
        """
        if cls.__doc__ is not None:
            return cls.__doc__
        else:
            return "No description available."

    @classmethod
    def url(cls) -> str:
        """
        Return the URL for the documentation of this heuristic.
        """
        return BASEURL+cls.identifier()

    @classmethod
    @abstractmethod
    def applies_to(cls, item) -> bool:
        """
        Checks if the heuristic can be applied to the given `item`.
        """

    @classmethod
    @abstractmethod
    def applies_to_types(cls) -> Sequence[type]:
        """
        Returns a list of types the heuristic can be applied to.
        """

    @classmethod
    @abstractmethod
    def passes(cls, item) -> bool:
        """
        A generic method that can apply the heuristic to any given item passed
        in. It is up to the caller to check if the `item` passed in is of a type
        the heuristic can be applied to, via the `applies_to()` method. This
        method will throw an exception if the heuristic does not apply to
        `item`.
        """

class HeuristicTypeException(Exception):
    """
    Exception thrown when a Heuristic cannot be applied to the `item` provided
    by its `passes()` method.
    """

    def __init__(self, cls: type[Heuristic], item: Any) -> None:
        super().__init__(
            f"Heuristic {cls.identifier()} does not apply to {type(item)}"
        )
