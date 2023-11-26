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
Importer for content OLX content. This will normally be an export of a course
from an Open edX installation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup
from lxml import etree

from doclint.structure.content import HTMLContent, Content
from doclint.structure.navigation import NavLevel


# =============================================================================
# (Data-)Classes
# =============================================================================

@dataclass
class Course(NavLevel):
    """
    A course and its metadata as well as its children, which are `Chapter`s.
    """
    url_name: str
    org: str
    chapters: list[Chapter]

    def is_root(self) -> bool:
        return True

    def has_children(self) -> bool:
        return len(self.chapters) > 0

    def children(self) -> list[NavLevel]:
        return self.chapters

    def has_content(self) -> bool:
        return False

    def content(self) -> list[Content]:
        return []


    @staticmethod # not sure if we need to switch this to classmethod?
    def read(datadir) -> Course:
        """
        Read course data including the chapters contained.
        """
        root = parse_xml(datadir.joinpath("course.xml"))
        assert root.tag == "course"

        course = Course(
            name = root.attrib['course'],
            parent = None,
            chapters = [],
            url_name = root.attrib['url_name'],
            org = root.attrib['org'],
        )
        course.chapters = course.read_chapters(datadir)
        return course


    def read_chapters(self, datadir: Path) -> list[Chapter]:
        """
        Read the XML file that lists the chapters contained in a course.
        """
        chapters: list[Chapter] = []
        root = parse_xml(datadir.joinpath(f'course/{self.url_name}.xml'))
        assert root.tag == 'course'

        for child in root.getchildren():
            if child.tag == 'chapter':
                chap_url_name = child.attrib['url_name']
                chapter = Chapter.read(datadir, chap_url_name, self)
                chapters.append(chapter)

        return chapters


@dataclass(kw_only=True)
class Chapter(NavLevel):
    """
    Chapter of a course, contains a number of Sequentials.
    """
    sequentials: list[Sequential]

    def is_root(self) -> bool:
        return False

    def has_children(self) -> bool:
        return len(self.sequentials) > 0

    def children(self) -> list[NavLevel]:
        return self.sequentials

    def has_content(self) -> bool:
        return False

    def content(self) -> list[Content]:
        return []

    def read(datadir: Path, url_name: str, parent: Course) -> Chapter:
        """
        Read the chapter definition for a chapter given by the `url_name`
        argument.
        """
        root = parse_xml(datadir.joinpath(f'chapter/{url_name}.xml'))

        chapter = Chapter(
            name = root.attrib['display_name'],
            sequentials = [],
            parent = parent
        )

        chapter.sequentials = [
            Sequential.read(datadir, sequential.attrib['url_name'], chapter)
                for sequential in root.getchildren()
        ]
        return chapter


@dataclass
class Sequential(NavLevel):
    """
    Learning sequence of units and activities, listed across the screen
    horizontally in Open edX.
    """
    verticals: list[Vertical]

    def is_root(self) -> bool:
        return False

    def has_children(self) -> bool:
        return len(self.verticals) > 0

    def children(self) -> list[NavLevel]:
        return self.verticals

    def has_content(self) -> bool:
        return False

    def content(self) -> list[Content]:
        return []

    def read(datadir: Path, url_name: str, parent: Chapter) -> Sequential:
        """
        Read a Sequential from disk.
        """
        root = parse_xml(datadir.joinpath(f'sequential/{url_name}.xml'))
        sequential = Sequential(
            name=root.attrib['display_name'],
            verticals=[],
            parent = parent
        )

        sequential.verticals = [
            Vertical.read(datadir, vertical.attrib['url_name'], sequential)
                for vertical in root.getchildren()
        ]

        return sequential


@dataclass
class Vertical(NavLevel):
    """
    A unit, video, etc.
    """
    elements: list = field(default_factory = list)

    def is_root(self) -> bool:
        return False

    def has_children(self) -> bool:
        return len(self.elements) > 0

    def children(self) -> list[NavLevel]:
        return self.elements

    def has_content(self) -> bool:
        return False

    def content(self) -> list[Content]:
        return []

    def read(datadir: Path, url_name: str, parent: Sequential) -> Vertical:
        """
        Read a vertical from disk.
        """
        root = parse_xml(datadir.joinpath(f'vertical/{url_name}.xml'))
        vertical = Vertical(
            name = root.attrib['display_name'],
            elements = [],
            parent = parent
        )

        vertical.elements = [
            Vertical.read_element(
                datadir,
                element.attrib['url_name'],
                element.tag,
                vertical
            )
            for element in root.getchildren()
        ]

        return vertical

    def read_element(
        datadir: Path,
        url_name: str,
        tagname: str,
        parent: Vertical
        ) -> HTMLUnit | Discussion | Video | Problem:
        """
        Depending on the specific type of element that is to be read,
        dispatches to a method to read that specific element type.
        """
        match tagname:
            case 'html':
                return HTMLUnit.read(datadir, url_name, parent)
            case 'discussion':
                pass
            case 'video':
                pass
            case 'problem':
                pass
        return None

@dataclass
class HTMLUnit(NavLevel):
    """
    An HTMLUnit in Open edX and the HTML it comprises. This is a leaf node
    in the navigation structure, so does not have any children but ony
    content.
    """
    html: HTMLContent

    def is_root(self) -> bool:
        return False

    def has_children(self) -> bool:
        return False

    def children(self) -> list[NavLevel]:
        return []

    def has_content(self) -> bool:
        return True

    def content(self) -> Content:
        return self.html


    def read(datadir: Path, url_name: str, parent: Vertical) -> HTMLUnit:
        """
        Read a Unit, comprising its metadata and HTML content
        """
        root = parse_xml(datadir.joinpath(f'html/{url_name}.xml'))
        htmlfile = datadir.joinpath(f'html/{url_name}.html')
        with open(htmlfile, 'r', encoding = 'utf-8') as fd:
            soup = BeautifulSoup(fd, features='lxml')
            unit = HTMLUnit(
                name = root.attrib['display_name']
                    if 'display_name' in root.attrib else None,
                parent = parent,
                html = []
            )
            unit.html.append(HTMLContent(content = soup, parent = unit))
            return unit


@dataclass
class Video(NavLevel):
    """
    A video in Open edX that is not just embedded in a Unit.
    """
    content: None # TODO


@dataclass
class Discussion(NavLevel):
    """
    A Discusssion
    """
    content: None # TODO


@dataclass
class Problem(NavLevel):
    """
    A Problem
    """
    content: None # TODO


# =============================================================================
# Module functions
# =============================================================================

def load(datadir: Path) -> Course:
    """
    Uses the static `read()` method in `Course` to read the course.xml file
    and from there anything else that is necessary to collect all course data.
    """
    return Course.read(datadir)


def parse_xml(file: Path):
    """
    Parse the xml from a file
    """
    with open(file, 'r', encoding='utf-8') as fd:
        xml = fd.read()

    return etree.fromstring(xml)