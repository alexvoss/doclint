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
Handling processing of the commandline arguments, printing help, etc.
"""

import argparse

# Setting up the argument parser used by the functions below.
parser = argparse.ArgumentParser(
    description='doclint arguments',
    add_help = False
)
parser.add_argument('report', type = str, nargs = '*',
        help = 'the report to run'
            +' - run doclint -h to see supported reports')
parser.add_argument('-d', '--docdir', type = str,
        help = 'the directory that contains the documentation')
parser.add_argument('-t', '--type', type=str,
                    help='the type of input data')
parser.add_argument('-o', '--output', type=str,
                    help='html file to output results to')
parser.add_argument('--types', action='store_true',
                    help='lists the content types available')
parser.add_argument('--reports', action='store_true',
                    help='list the reports avialable')
parser.add_argument('--heuristics', action='store_true',
                    help='list the heuristics available')
parser.add_argument('-h', '--help', action='store_true',
                    help='print help and exit')

def parse_args() -> argparse.Namespace:
    """
    Parse the command-line arguments and return them to the caller. Print help
    information if arguments are invalid and then exit. Print help and exit if
    the -h / --help argument is given.
    """
    args = parser.parse_args()
    return args

def print_help():
    """
    Print the standard help. Used when the -h option is used but
    """
    parser.print_help

def list_types(types):
    """
    Lists the available content types
    """
    pass