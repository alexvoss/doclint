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
Methods to dynamically load extensions for doclint. These are heuristics,
plugins and reports.
"""

import importlib
import inspect
import glob
import os

from pathlib import Path

def find_datatypes() -> dict:
    """
    Find plugins that adapt doclint to different sources of data.
    """
    datatypes = {}
    datatypes_path = get_install_path().joinpath('datatypes')
    datatype_files = find_python_files([datatypes_path])
    for datatype_file in datatype_files:
        datatypes[datatype_file.stem] = datatype_file
    return datatypes

def find_heuristics() -> dict:
    """
    Heuristics provide the functionality to automatically check content.
    """
    heuristics = {}
    heuristics_path = get_install_path().joinpath('heuristics')
    heuristic_files = find_python_files([heuristics_path])
    for heuristic_file in heuristic_files:
        heuristics[heuristic_file.stem] = heuristic_file
    return heuristics

def import_reports() -> dict:
    """
    Reports bundle the execution and presentation of heuristics into
    reports for specific purposes.
    """
    reports = {}
    reports_path = get_install_path().joinpath('reports')
    report_files = find_python_files([reports_path])
    for report_file in report_files:
        reports[report_file.stem] = report_file
    return reports

def import_hooks() -> dict:
    """
    Hooks augment the tool by implementing specific callback functions.
    """
    # TODO: implement, this will be slightly different from the other ones
    # hooks = find_python_files([get_hooks_path()])
    return {}


def get_install_path() -> Path:
    """
    Returns the path to the installed doclint package.
    """
    path = Path(inspect.getfile(get_install_path)).parent.parent
    return path

def get_hooks_path() -> Path | None:
    """
    Return the path to the user-configurable hooks. This is controlled by a
    command-line argument so we do not execute random Python files.
    """
    return None

def find_python_files(paths: list[Path]) -> list[Path]:
    """
    Find all the Python source files at the given paths, excluding those
    with the filename `__init__.py`. Returns a list of absolute paths to
    those files.
    """
    modules: list[Path] = []
    for path in paths:
        found = glob.glob('**/*.py', root_dir=path, recursive=True)
        found = [path.joinpath(module) for module in found
            if os.path.basename(module) != '__init__.py']
        modules += found
    return modules

def import_modules(name: str, python_files: list[Path]):
    """
    Given the name of a parent module and a list of detected Python files,
    imports these as children so that their functions can be called.
    """
    for file in python_files:
        modname = name + '.' + file.stem
        importlib.import_module(modname)
