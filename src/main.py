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
doclint is a commandline tool that runs a set of automated reports on your
documentation. The aim in all cases is to apply heuristics to improve the
quality of your documentation. Some reports rely on automated heuristics while
others simply provide a way to look at aspects of the documentation so that
heuristics can be manually applied.

The tool comes with a number of integrations. Supported at the moment are:

- Material for MkDocs
- Open edX

"""

# TODO: move some of this functionality into the doclint package.

import importlib
import sys

from pathlib import Path

import doclint.util.extensions as extensions
import doclint.util.cli as cli

datatypes: dict = extensions.find_datatypes()
heuristics: dict = extensions.find_heuristics()
reports: dict = extensions.import_reports()
hooks: dict = extensions.import_hooks()


def main():
    """
    main() method called when this is run as a program (as opposed to used
    as a library).
    """

    args = cli.parse_args()
    if args.help:
        if args.report:
            for report in args.report:
                print_report_help(report) # help for a specific report
        else:
            cli.print_help() # general help
    else:
        data = read_data(args.type, Path(args.docdir))
        for report in args.report:
            output = Path(args.output).joinpath(report+".html") \
                if args.output else None
            run_report(report, data, output)


def read_data(datatype: str, docdir: Path):
    """
    Load data from the docdir provided using the given document loader
    """
    modname = 'doclint.datatypes.'+datatype
    importlib.import_module(modname)
    dataloader = sys.modules[modname]
    return dataloader.load(docdir)


def run_report(report: str, data, output):
    """
    Load the report module and run the report.
    """
    modname = 'doclint.reports.'+report
    importlib.import_module(modname)
    reporter = sys.modules[modname]
    reporter.report(data, output)


def print_report_help(report: str):
    """
    Prints the help for the report selected.
    """
    if not report in reports:
        print(f"error: report {report} not found.")
        sys.exit(1)

    modname = 'doclint.reports.'+report
    importlib.import_module(modname)
    module = sys.modules[modname]
    module.print_help()


def check_args(args):
    """
    Checks that the arguments provided are valid. The aim of including this
    explicit step is to be able to provide nice, user-friendly output when
    something goes wrong and to do this at the earliest point possible.
    """
    check_type(args)
    check_report(args)


def check_type(args):
    """
    Checks that the `-t/--type` argument matches a module under
    `doclint.datatypes`.
    """
    # TODO: implement this check
    datatype = args.type

def check_report(args):
    """
    Checks that the `report` arguments match modules under `doctlint.reports`.
    """
    # TODO: implement this check
    for report in args.report:
        pass


# if run as a script, call main()
if __name__ == "__main__":
    main()
