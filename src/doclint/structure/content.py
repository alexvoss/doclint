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
Abstract base class for defining content in the documentation.
"""

from __future__ import annotations

from typing import Any, Sequence
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class Content(ABC):
    """
    A base class for representing content of different kinds.
    """

    parent: Any # avoiding circular import with navigation

    @abstractmethod
    def links(self) -> list[Link]:
        """
        Return any links contained in the content.
        """

    @abstractmethod
    def text(self) -> list[Text]:
        """
        Return a list of the text elements in the content.
        """

@dataclass
class HTMLContent(Content):
    """
    HTML content parsed by BeautifulSoup.
    """

    content: BeautifulSoup

    def links(self) -> Sequence[Link]:
        links = []
        for link in self.content.find_all('a', recursive = True):
            links.append(Link(
                text = link.get_text(),
                url = link.get('href'),
                attrs = link.attrs
            ))
        return links
    
    def images(self) -> Sequence[Image]:
        images = []
        for image in self.content.find_all('img', recursive = True):
            images.append(Image(
                src = image.get('src'),
                alt_text = image.get('alt') 
            ))
        return images

    def text(self) -> list[Text]:
        return [] # TODO


@dataclass
class Link:
    """
    A link with the URL, link text and any attributes.
    """
    text: str
    url: str
    attrs: dict[str, str]


@dataclass
class Image:
    """
    An image.
    """
    src: str
    alt_text: str

    def get_dimensions():
        """
        Get the width and height in pixels.
        """
        pass

    def get_size():
        """
        Get the size in Megabytes.
        """
        pass

@dataclass
class Text:
    """
    A chunk of text in the content. Could be anyting from a single letter to
    a paragraph or even a whole text.
    """
    text: str

@dataclass
class VideoContent(Content):
    """
    A video that is embedded in the content, either locally or hosted on a
    remote service.
    """

    name: str
    local: bool
    hoster: str
    src: str
    transcripts: list[dict[str, str]] # mapping languages to filenames
    
    def links(self) -> list[Link]:
        return []
    
    def text(self) -> list[Text]:
        return []
    
@dataclass
class DiscussionContent(Content):
    """
    A discussion 
    """

    def links(self) -> list[Link]:
        return []
    
    def text(self) -> list[Text]:
        return []

@dataclass 
class ProblemContent(Content):
    """
    A problem definition.
    """
    name: str
    type: str
    label: str

    def links(self) -> list[Link]:
        return []
    
    def text(self) -> list[Text]:
        return []
    
@dataclass
class UnknownContent(Content):
    
    def links(self) -> list[Link]:
        return []
    
    def text(self) -> list[Text]:
        return []